from src.sender import send
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Send message via audio.")
    parser.add_argument("message", nargs="?", help="Message to send (e.g. 'hello world').")
    args = parser.parse_args()

    if not args.message:
        print("No message provided. Please provide a message to send.")
        exit(1)

    print(f"Sending message: {args.message}")
    send(args.message)