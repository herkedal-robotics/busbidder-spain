# BusBidder Spain

BusBidder Spain is a Python command-line application for comparing and booking fictional bus journeys in Spain.

The application allows users to search for bus tickets from Madrid to 15 destinations. It compares offers from five fictional bus companies and ranks them based on the user's preferences.

## 1. Main Features

- Search for bus journeys from Madrid to different Spanish destinations.
- Filter offers by destination, travel dates, budget, departure time, transfers, journey duration, luggage, and ticket conditions.
- Rank offers using four criteria: price, duration, departure time, and ticket flexibility.
- Choose between three traveler profiles: Budget, Business, and Flexible Tourist.
- Enter custom ranking weights.
- Display advantages and disadvantages of offers.
- Book a ticket and receive a unique booking reference.
- Check an existing booking using its reference number.
- Save bookings and update the number of available seats.
- Save important events and errors in a log file.

## 2. Requirements

- Python 3.14.5 (version used for development and testing).
- No external Python libraries are currently required.

The application uses Python standard-library modules such as `csv`, `datetime`, `pathlib`, `re`, and `logging`.

## 3. Running the Program

Open PowerShell or a terminal and navigate to the folder containing `main.py`.

Run:

```powershell
python main.py
```

On Windows, you can also try:

```powershell
py main.py
```

If Python is not available through these commands, use the full path to your Python executable. For example, on the development computer, the application was run using:

```powershell
& "C:\Users\herke\AppData\Local\Programs\Python\Python314\python.exe" main.py
```

The main menu allows the user to search for offers, view destinations, check bookings, or exit.

During input, the user can enter:

- `c` or `back` to cancel and return.
- `e` or `exit` to quit the application.

## 4. Running Tests

Automated tests are stored in `tests.py`.

Open PowerShell or a terminal and navigate to the folder containing `tests.py`.

Run:

```powershell
python tests.py
```

On Windows, you can also try:

```powershell
py tests.py
```

If Python is not available through these commands, use the full path to your Python executable. For example, on the development computer, the tests were run using:

```powershell
& "C:\Users\herke\AppData\Local\Programs\Python\Python314\python.exe" tests.py
```

The tests cover several parts of the application, including data validation, offer filtering, ranking, booking, file saving, and error handling.

The tests print `PASS` messages when the checked behavior works correctly.

## 5. Data Files

The application uses CSV files stored in the `data` folder.

| File | Description |
|---|---|
| `companies.csv` | Five fictional bus companies |
| `destinations.csv` | Fifteen destinations from Madrid |
| `offers.csv` | Generated bus offers, prices, dates, and available seats |
| `bookings.csv` | Saved bookings and fare conditions |

The application can generate offers and save them to CSV files.

The file `busbidder.log` records selected program events and errors.

## 6. Project Structure

| File | Purpose |
|---|---|
| `main.py` | Main menu and user interaction |
| `bus_company.py` | Bus company information and reviews |
| `destination.py` | Destination information |
| `bus_offer.py` | Bus offers and validation |
| `review.py` | Customer rating class |
| `booking.py` | Booking information and references |
| `offer_generator.py` | Generation of fictional offers |
| `offer_search.py` | Filtering bus offers |
| `offer_ranking.py` | Weighted scoring and ranking |
| `csv_loader.py` | Reading and writing CSV files |
| `logging_utils.py` | Logging decorator |
| `exceptions.py` | Custom exceptions |
| `tests.py` | Automated tests |

## 7. Ranking System

The application ranks acceptable offers using four criteria:

- **Price:** cheaper offers receive higher scores.
- **Duration:** shorter journeys receive higher scores.
- **Departure time:** offers closer to the preferred departure time receive higher scores.
- **Flexibility:** changeable and refundable tickets receive higher scores.

Each criterion receives a score between 0 and 100.

The final score is calculated using a weighted sum. Users can choose a predefined traveler profile or provide their own weights.

Only offers that satisfy the mandatory search requirements are ranked.

## 8. Booking System

After comparing offers, the user can select a ticket and confirm a booking.

The program checks seat availability, generates a booking reference, saves the booking, and reduces the number of available seats.

The booking also stores the ticket's luggage, refund, and change conditions.

Bookings can be retrieved using their reference numbers.

## 9. Limitations

- The companies and offers are fictional.
- The application does not process real payments.
- Reviews can be created in Python, but passengers cannot submit them through the menu.
- Reviews are not saved between program runs.
- Booking references are not protected by user authentication.
- CSV files are not designed for multiple users booking at the same time.

## 10. Additional Information

The final project report contains the architecture diagram, testing results, traveler-profile comparisons, design decisions, limitations, and declaration of AI assistance.