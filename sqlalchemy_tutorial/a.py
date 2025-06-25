import csv

def load_data(file_path):
    with open(file_path, mode='r') as file:
        reader = csv.reader(file)
        data = list(reader)
    return data

if __name__ == "__main__":
    # This block will only execute if data_loader.py is executed directly
    data = load_data("/home/surendhar/Downloads/gender_submission.csv")
    print("Data loaded successfully!")
    print(data)
