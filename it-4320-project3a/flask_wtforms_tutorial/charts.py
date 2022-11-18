'''
This web service extends the Alphavantage api by creating a visualization module, 
converting json query results retuned from the api into charts and other graphics. 

This is where you should add your code to function query the api
'''
import requests
from datetime import datetime, timedelta
from datetime import date
import pygal


#Helper function for converting date
def convert_date(str_date):
    return datetime.strptime(str_date, '%Y-%m-%d').date()

# Function to assign time series for JSON
def jsonTime(timeOption):
    if (timeOption == "1"):
        return "Time Series (5min)"
    elif (timeOption == "2"):
        return "Time Series (Daily)"
    elif (timeOption == "3"):
        return "Weekly Time Series"
    elif (timeOption == "4"):
        return "Monthly Time Series"

def queryAPI(functionType, symbol, outputSize, key):
    # URL construction for API request
    # If time series is intraday, assign alternate url for correct API request
    if(functionType == "1"):
        functionType = "TIME_SERIES_INTRADAY"
        url = "https://www.alphavantage.co/query?function=" + functionType + "&symbol=" + symbol +"&interval=5min&outputsize=" + outputSize + "&apikey=" + key
    # If time series is not intraday, assign this URL
    elif(functionType == "2"):
        functionType = "TIME_SERIES_DAILY_ADJUSTED"
        url = "https://www.alphavantage.co/query?function=" + functionType + "&symbol=" + symbol + "&outputsize=" + outputSize + "&apikey=" + key
    elif(functionType == "3"):
        functionType = "TIME_SERIES_WEEKLY"
        url = "https://www.alphavantage.co/query?function=" + functionType + "&symbol=" + symbol + "&outputsize=" + outputSize + "&apikey=" + key
    elif(functionType == "4"):
        functionType = "TIME_SERIES_MONTHLY"
        url = "https://www.alphavantage.co/query?function=" + functionType + "&symbol=" + symbol + "&outputsize=" + outputSize + "&apikey=" + key
    # Query API
    response = requests.request("GET", url)
    # Format data as JSON object
    data = response.json()
    # Return data
    return data

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
        #startDate = datetime.datetime.strptime(str(startDate) + ' 00:00:00', '%Y-%m-%d %H:%M:%S')
        #endDate = datetime.datetime.strptime(str(endDate) + ' 00:00:00', '%Y-%m-%d %H:%M:%S')
        #delta = datetime.timedelta(minutes=5)
        startDate = datetime.strptime(str(startDate) + ' 00:00:00', '%Y-%m-%d %H:%M:%S')
        endDate = datetime.strptime(str(endDate) + ' 00:00:00', '%Y-%m-%d %H:%M:%S')
        #delta = datetime.timedelta(minutes=5)
        delta = timedelta(minutes=5)
    else:
        #delta = datetime.timedelta(days=1)
        delta = timedelta(days=1)
    # If line chart is selected
    if (chartType == "2"):
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
        #lineChart.render_in_browser()
        return lineChart.render_data_uri()
    # If bar chart is selected
    if (chartType == "1"):
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
        #barChart.render_in_browser()
        return barChart.render_data_uri()

