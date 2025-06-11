from src.receiver import receive

if __name__ == "__main__":
    try:
        receive()
    except KeyboardInterrupt:
        print(f"\nReceiver stopped by user.")