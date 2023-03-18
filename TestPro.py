# импортируем необходимые библиотеки
import openai
import csv
import os

# инициализируем аутентификацию API
openai.api_key = "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"

def analyze_reviews():
    # получаем название файла
    filename = 'reviews.csv'

    # проверяем, что файл существует
    if not os.path.isfile(filename):
        print(f"File {filename} does not exist")
        return

    # определяем fieldnames
    fieldnames = ["email", "review text", "date", "rate"]

    try:
        # открываем файл с отзывами, создаем новый файл для записи результатов и записываем header
        with open(filename, newline='') as csvfile,\
                open(f"{os.path.splitext(filename)[0]}_analyzed.csv", mode='w', newline='') as csvfile_out:
            reader = csv.DictReader(csvfile, delimiter=',')
            writer = csv.DictWriter(csvfile_out, fieldnames=fieldnames)
            writer.writeheader()

            # оцениваем каждый отзыв и записываем его в новый файл
            for row in reader:
                review = row.get('review text', '')
                response = openai.Completion.create(
                    engine="gpt-3.5-turbo",
                    prompt=f"Please rate the following review on a scale from 1 to 10, where 10 is the most positive and 1 is the most negative.\n\nReview: {review.replace(',', '').replace('', '')}\nRating:",
                    temperature=0.5,
                    max_tokens=1,
                )

                if response["choices"][0]["text"] is not None and response["choices"][0]["text"].isdigit():
                    rating = int(response["choices"][0]["text"])
                    rating = min(max(rating, 1), 10)
                    row['rate'] = str(rating)
                else:
                    row['rate'] = ''

                writer.writerow(row)

        # сортируем отзывы по убыванию оценки и записываем их в новый файл
        with open(f"{os.path.splitext(filename)[0]}_analyzed.csv", newline='') as csvfile,\
                open(f"{os.path.splitext(filename)[0]}_analyzed_sorted.csv", mode='w', newline='') as csvfile_out:
            reader = csv.DictReader(csvfile)
            rows = sorted(reader, key=lambda x: int(x.get('rate', 0)), reverse=True)

            writer = csv.DictWriter(csvfile_out, fieldnames=fieldnames)
            writer.writeheader()

            for row in rows:
                writer.writerow(row)
    except ValueError as e:
        print(f"An error occurred: {e}")
        return

    print(f"Analysis completed. Results saved in {os.path.splitext(filename)[0]}_analyzed_sorted.csv")

analyze_reviews()