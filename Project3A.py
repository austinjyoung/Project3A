import json
import requests
import pygal
import datetime
from dateutil.relativedelta import relativedelta

# Global variable for while loop
run = True

# Function to to supply prompt and get user input
def userInput(prompt, inputText):
    # Prompt user
    print(prompt)
    # Get user input
    selection = input(inputText)
    # Return user input
    return selection

# Function to get user input for chart type
def chartSelection(invalidInputText):
    # User input prompt variable
    prompt = "Select the chart you would like from the following options:\n1. Line Chart\n2. Bar Chart\n"
    # Input text variable
    inputText = "Enter the chart type (1, 2): "
    # Call userInput function
    selection = userInput(prompt, inputText)
    # If user selection is not a given option, prompt user to try again
    while (selection != "1" and selection != "2"):
        selection = userInput("", invalidInputText)
    if (selection == "1"):
        return "line"
    elif (selection == "2"):
        return "bar"

# Function to get user input for time series selection
def timeSeries(invalidInputText):
    # User input prompt variable
    prompt = "Select the Time Series of the chart you want to generate:\n1. Intraday\n2. Daily\n3. Weekly\n4. Monthly\n"
    # Input Text variable
    inputText = "Enter the time series option (1, 2, 3, 4): "
    selection = userInput(prompt, inputText)
    # If user selection is not a given option, prompt user to try again
    while (selection != "1" and selection != "2" and selection != "3" and selection != "4"):
        selection = userInput("", invalidInputText)
    if (selection == "1"):
        return "TIME_SERIES_INTRADAY"
    if (selection == "2"):
        return "TIME_SERIES_DAILY"
    if (selection == "3"):
        return "TIME_SERIES_WEEKLY"
    if (selection == "4"):
        return "TIME_SERIES_MONTHLY"

# Function to get user input for start date
def startDate(dateErrorPrompt):
    date_format = '%Y-%m-%d'
    inputText = "Enter the start Date (YYYY-MM-DD): "
    selection = userInput("", inputText)
    # using try-except blocks for handling the exceptions
    while True:
        try:
            # formatting the date using strptime() function
            dateObject = datetime.datetime.strptime(selection, date_format).date()
            # If the date validation goes wrong
        except ValueError:
            # printing the appropriate text if ValueError occurs
            selection = userInput(dateErrorPrompt, inputText)
        else:
            #No error, break loop
            break
    return dateObject

# Function to get user input for end date
def endDate(dateErrorPrompt):
    date_format = '%Y-%m-%d'
    inputText = "Enter the end Date (YYYY-MM-DD): "
    selection = userInput("", inputText)
    # using try-except blocks for handling the exceptions
    while True:
        try:
            # formatting the date using strptime() function
            dateObject = datetime.datetime.strptime(selection, date_format).date()
            # If the date validation goes wrong
        except ValueError:
            # printing the appropriate text if ValueError occurs
            selection = userInput(dateErrorPrompt, inputText)
        else:
            # No error, break loop
            break
    return dateObject

# Function to parse data
def parseData(data, timeSeries, date):
    # Cast date as string
    date = str(date)
    try:
        # Assign data values to variables
        open = data[timeSeries][date]["1. open"]
        high = data[timeSeries][date]["2. high"]
        low = data[timeSeries][date]["3. low"]
        close = data[timeSeries][date]["4. close"]
    # If no data in entry, assign None values
    except KeyError:
        open = None
        close = None
        low = None
        high = None
    return open, high, low, close

# Function to assign time series for JSON
def jsonTime(timeOption):
    if (timeOption == "TIME_SERIES_INTRADAY"):
        return "Time Series (5min)"
    elif (timeOption == "TIME_SERIES_DAILY"):
        return "Time Series (Daily)"
    elif (timeOption == "TIME_SERIES_WEEKLY"):
        return "Weekly Time Series"
    elif (timeOption == "TIME_SERIES_MONTHLY"):
        return "Monthly Time Series"

# Function to build chart
def buildChart(user_symbol, chartType, data, timeSeries, startDate, endDate):
    # Variable for iterating dictionary
    i = 0
    
    # Variables for assigning start and end dates to graph title
    tmpStart = startDate
    tmpEnd = endDate
    
    # Variable for graph title assignment
    graphTitle = 'Stock Data for ' + user_symbol + ": " + str(tmpStart) + " to " + str(tmpEnd)
    
    # Lists for adding values to graphs
    openList = []
    closeList = []
    highList = []
    lowList = []
    dateList = []
    # Delta time for date iteration
    if(timeSeries == "Time Series (5min)"):
        startDate = datetime.datetime.strptime(str(startDate) + ' 00:00:00', '%Y-%m-%d %H:%M:%S')
        endDate = datetime.datetime.strptime(str(endDate) + ' 00:00:00', '%Y-%m-%d %H:%M:%S')
        delta = datetime.timedelta(minutes=5)
    else:
        delta = datetime.timedelta(days=1)
    # If line chart is selected
    if (chartType == "line"):
        # Create line chart
        lineChart = pygal.Line()
        # For all data entries, iterate and add to list
        while(startDate <= endDate):
            open, high, low, close = parseData(data, timeSeries, startDate)
            # If no data available for date, skip
            if(open == None and high == None and low == None and close == None):
                startDate += delta
                continue
            # Add data to lists
            openList.append(float(open))
            closeList.append(float(close))
            highList.append(float(high))
            lowList.append(float(low))
            dateList.append(startDate)
            # Increment datetime
            startDate += delta
        # Add elements to graph
        lineChart.add("Open", openList)
        lineChart.add("Close", closeList)
        lineChart.add("High", highList)
        lineChart.add("Low", lowList)
        # Render graph in browser
        lineChart.title = graphTitle
        lineChart.x_labels = dateList
        lineChart.render_in_browser()
    # If bar chart is selected
    if (chartType == "bar"):
        # Create bar chart
        barChart = pygal.Bar()
        # For all data entries, iterate and add to list
        while(startDate <= endDate):
            open, high, low, close = parseData(data, timeSeries, startDate)
            # If no data available for date, skip
            if(open == None and high == None and low == None and close == None):
                startDate += delta
                continue
            # Add data to lists
            openList.append(float(open))
            closeList.append(float(close))
            highList.append(float(high))
            lowList.append(float(low))
            dateList.append(startDate)
            # Increment datetime
            startDate += delta
        # Add elements to graph
        barChart.add("Open", openList)
        barChart.add("Close", closeList)
        barChart.add("High", highList)
        barChart.add("Low", lowList)
        # Render graph in browser
        barChart.title = graphTitle
        barChart.x_labels = dateList
        barChart.render_in_browser()
    # Error handling
    elif (chartType != "line" and chartType != "bar"):
        # Error message
        print("ERROR")

# Function to get data from the API
def queryAPI(functionType, symbol, outputSize, key):
    # URL construction for API request
    # If time series is intraday, assign alternate url for correct API request
    if(functionType == "TIME_SERIES_INTRADAY"):
        url = "https://www.alphavantage.co/query?function=" + functionType + "&symbol=" + symbol +"&interval=5min&outputsize=" + outputSize + "&apikey=" + key
    # If time series is not intraday, assign this URL
    else:
        url = "https://www.alphavantage.co/query?function=" + functionType + "&symbol=" + symbol + "&outputsize=" + outputSize + "&apikey=" + key
    # Query API
    response = requests.request("GET", url)
    # Format data as JSON object
    data = response.json()
    # Return data
    return data

# While loop to run program and allow for repetition
while (run == True):
    # Variable for invalid selection input text
    invalidInputText = "Invalid option! Enter the number of the option you want to select: "
    invalidInputDatesFormat = "Invalid date! Enter the date in YYYY-MM-DD format:  "
    # Variable for date error prompt
    dateErrorPrompt = "\nIncorrect date format. Enter the start Date in YYYY-MM-DD format"
    
    # Variables for output size and API key parameters
    outputSize = "full"
    key = "DLEZPCELNFARX2UF"

    # Print menu
    print("\nStock Data Visualizer")
    print("----------------------")

    # Ask the user for the stock symbol they would like to visualize
    user_symbol = input("Enter the stock symbol you are looking for: ")

    # Call function for chart selection and assign value ("line" or "bar")
    # This value will be used to open the correct chart in the browser
    chartOption = chartSelection(invalidInputText)

    # Call function for time series selection and assign value
    functionType = timeSeries(invalidInputText)

    # Call function for start date
    startTime = startDate(dateErrorPrompt)

    # Call function for end date
    endTime = endDate(dateErrorPrompt)

    # Checks to see if start time value is after endtime and resets if true
    while (startTime >= endTime):
        print("Start date cannot be later than or equal to End date. Enter the dates again.")
        startTime = startDate(dateErrorPrompt)
        endTime = endDate(dateErrorPrompt)

    # Assign correct format for JSON based on user selection
    jTime = jsonTime(functionType)

    # Pass the symbol to the queryAPI function
    data = queryAPI(functionType, user_symbol, outputSize, key)

    # Builds chart and opens it in browser
    buildChart(user_symbol, chartOption, data, jTime, startTime, endTime)
    
    # Check if the user would like to visualize another stock
    user_continue = input("Would you like to view more stock data?\n Press 'y' to continue: ")
    if (user_continue == "y"):
        # Repeat program by iterating through while loop again
        run = True
    else:
        # End program