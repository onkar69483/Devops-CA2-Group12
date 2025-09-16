from predict import predict

def create_submission():
    predictions = predict()
    predictions.to_csv("submission.csv", index=False)
    print("submission.csv created.")

if __name__ == "__main__":
    create_submission()