from a import load_data

def process_data(data):
    # Imagine this is where you clean/process your data
    processed_data = [row[0] for row in data]  # Simplified for the example
    return processed_data

if __name__ == "__main__":
    # Entry point for testing data processing
    data = load_data("/home/surendhar/Downloads/gender_submission.csv")
    processed_data = process_data(data)
    print("Processed data:", processed_data)
