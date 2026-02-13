import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from peft import PeftModel
import os
import sys
import time

class ModelInterface:
    def __init__(self):
        self.tokenizer = None
        self.sentiment_model = None
        self.topic_model = None
        self.model_checkpoint = "distilbert-base-uncased"

    def load_models(self):
        """Load tokenizer and models with error handling"""
        try:
            print("Loading models and tokenizer...")
            # Load tokenizer
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_checkpoint)

            # Load sentimen model
            if os.path.exists("./lora-sentiment"):
                base_model_sentiment = (
                        AutoModelForSequenceClassification.from_pretrained(self.model_checkpoint, num_labels=2)
                    )
                self.sentiment_model = PeftModel.from_pretrained(base_model_sentiment, "./lora-sentiment")
                self.sentiment_model.eval()
            else:
                raise FileNotFoundError("Sentiment model checkpoint not found at './lora-sentiment'")

            # Load topic model
            if os.path.exists("./lora-topic"):
                base_model_topic = (
                        AutoModelForSequenceClassification.from_pretrained(self.model_checkpoint, num_labels=4)
                    )
                self.topic_model = PeftModel.from_pretrained(base_model_topic, "./lora-topic")
                self.topic_model.eval()
            else:
                raise FileNotFoundError("Topic model checkpoint not found at './lora-topic'")

            print("Models and tokenizer loaded successfully.")
        except Exception as e:
            print(f"Error loading models: {e}")
            sys.exit(1)

    def analyze_text(self, text, model_type="both"):
        """Analyze text with specified model type"""
        if not text.strip():
            return None

        inputs = self.tokenizer(
                text.lower().strip(),
                return_tensors="pt",
                truncation=True,
                max_length=128
            )

        results = {}

        try:
            if model_type in ["sentiment", "both"]:
                with torch.no_grad():
                    outputs = self.sentiment_model(**inputs)
                    sentiments_probs = torch.nn.functional.softmax(outputs.logits, dim=-1).item()
                    sentiment_pred = torch.argmax(sentiments_probs, dim=-1).item()
                    sentiment_conf = sentiments_probs[0][sentiment_pred].item()

                    sentiment_map = {0: "negative", 1: "positive"}
                    results["sentiment"] = {
                            "prediction": sentiment_map.get(sentiment_pred, "unknown"),
                            "confidence": sentiment_conf
                        }

            if model_type in ["topic", "both"]:
                with torch.no_grad():
                    outputs = self.topic_model(**inputs)
                    topic_probs = torch.nn.functional.softmax(outputs.logits, dim=-1).item()
                    topic_pred = torch.argmax(topic_probs, dim=-1).item()
                    topic_conf = topic_probs[0][topic_pred].item()

                    topic_map = {0: "world", 1: "sports", 2: "business", 3: "science/tech"}
                    results["topic"] = {
                            "prediction": topic_map.get(topic_pred, "unknown"),
                            "confidence": topic_conf
                        }
            return results
        except Exception as e:
            print(f"Error during analysis: {e}")
            return None

def print_welcome():
    print("\n" + "="*50)
    print("Welcome to the LoRA Model Chat Interface!")
    print("\n" + "="*50)
    print("\nThis interface allows you to analyze text for:")
    print("1. Sentiment Analysis (positive/negative)")
    print("2. Topic Classification (world, sports, business, science/tech)")
    print("\nCommands:")
    print("- Type 'quit' or 'exit' to end the session.")
    print("- Type 'switch' to toggle between sentiment and topic analysis.")
    print("- Type 'help' to see this instructions again.")
    print("="*50 + "\n")

def chat_interface():
    """Main chat interface function"""
    interface = ModelInterface()

    print("Initializing models, please wait...")
    if not interface.load_models():
        print("Failed to load models. Exiting.")
        return

    print_welcome()
    mode = "both"

    while True:
        try:
            print(f"\nCurrent mode: {mode}")
            text = input("Enter text to analyze (or command): ").strip()

            # Handle commands
            if text.lower() in ["quit", "exit"]:
                print("Exiting the chat interface. Goodbye!")
                break
            elif text.lower() == "help":
                print_welcome()
                continue
            elif text.lower() == "switch":
                while True:
                    new_mode = input("Enter new mode (sentiment/topic/both): ").strip().lower()
                    if new_mode in ["sentiment", "topic", "both"]:
                        mode = new_mode
                        print(f"Switched to {mode} mode.")
                        break
                    else:
                        print("Invalid mode. Please enter 'sentiment', 'topic', or 'both'.")
                continue

            if not text:
                print("Please enter some text to analyze.")
                continue

            # Analyze text
            print("Analyzing text, please wait...")
            results = interface.analyze_text(text, model_type=mode)

            if results:
                print("\nAnalysis Results:")
                if "sentiment" in results:
                    sent_result = results["sentiment"]
                    print(f"Sentiment: {sent_result['prediction']} (Confidence: {sent_result['confidence']:.2f})", end="")
                if "topic" in results:
                    topic_result = results["topic"]
                    print(f"Topic: {topic_result['prediction']} (Confidence: {topic_result['confidence']:.2f})", end="")
            else:
                print("No results returned from analysis. Please try again...")

        except KeyboardInterrupt:
            print("\nExiting the chat interface. Goodbye!")
            break
        except Exception as e:
            print(f"An error occurred: {e}")
            print("Please try again...")

if __name__ == "__main__":
    chat_interface()

