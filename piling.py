# online stock piling
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import pickle
pd.core.common.is_list_like = pd.api.types.is_list_like


def update(a):
	for key, value in dict.items(a):
		a[key] = value - timedelta(days = 1)
	return a
	
def red(a,st):
	if a < datetime.now():
		return u"<font color="+u"red"+"><b>"+str(st)+u"</b></font>"
	elif a < datetime.now() + timedelta(days = 2):
		return u"<font color="+u"orange"+"><b>"+str(st)+u"</b></font>"
	else:
		return str(st)
	
def to_list(a):
	dictlist = list()
	sortedkeys = sorted(a, key=str.lower)
	for key in sortedkeys:
		temp1 = key
		temp2 = "{:%B %d, %Y}".format(a[key])
		temp2 = red(a[key],temp2)
		dictlist.append(temp1)
		dictlist.append(temp2)
	
	return dictlist
	
def p(key,delta):
	global a
	a[key] = datetime.now() + timedelta(days=delta)
	
def pp(key):
	global a 
	del a[key]
	
def generate_html_with_table(data, columns_or_rows = 1, \
                             column_name_prefix = 'Column', \
                             span_axis = 1, \
                             showOutput = True):
    """
    This function returns a pandas.DataFrame object and a 
    generated html from the data based on user specifications.
    
    #Example:
      data_html, data_df = generate_html_with_table(data, columns_or_rows, column_name_prefix, span_axis, showOutput)
      # To suppress output and skip the DataFrame:
      # span data along a row first
        columns = 4
        columns_or_rows = columns
        data_html, _ = generate_html_with_table(data, columns_or_rows, column_name_prefix, 1, False)  
      # span data along a column first
        rows = 4
        columns_or_rows = rows
        data_html, _ = generate_html_with_table(data, columns_or_rows, column_name_prefix, 0, False)   
      
    # Inputs: 
        1. data:               Data
           (dtype: list)
           
      **Optional Input Parameters:**
        2. columns_or_rows:            Number of Columns or rows
           (dtype: int)                columns: span_axis = 1
           (DEFAULT: 1)                rows:    span_axis = 0
        3. column_name_prefix: The Prefix for Column headers
           (dtype: string)
           (DEFAULT: 'Column')
        4. span_axis:          The direction along which the elements span.
           (dtype: int)        span_axis = 0 (span along 1st column, then 2nd column and so on)
           (DEFAULT: 1)        span_axis = 1 (span along 1st row, then 2nd row and so on)
        5. showOutput:         (True/False) Whether to show output or not. Use 
           (dtype: boolean)                   False to suppress printing output.
           (DEFAULT: True)
                                                              
    # Outputs:
        data_html: generated html
        data_df:   generated pandas.DataFrame object
        
    # Author: Sugato Ray 
    Github: https://github.com/sugatoray
    Repository/Project: CodeSnippets
    
    """
    # Calculate number of elements in the list: data
    elements = len(data)
    # Calculate the number of rows/columns needed
    if (span_axis == 0): # if spanning along a column
      rows = columns_or_rows
      columns = int(np.ceil(elements/rows))    
    else: #(span_axis = 1)
      columns = columns_or_rows
      rows = int(np.ceil(elements/columns))
    # Generate Column Names
    column_names = [column_name_prefix + '_{}'.format(i) \
                    for i in np.arange(columns)]    
    # Convert the data into a numpy array    
    data_array = np.array(data + ['']*(columns*rows - elements))		
    if (span_axis == 0):
      data_array = data_array.reshape(columns,rows).T  
    else: #(span_axis == 0)
      data_array = data_array.reshape(rows,columns)  
    
    # Convert the numpy array into a pandas DataFrame
    data_df = pd.DataFrame(data_array, columns = column_names) 
    # Create HTML from the DataFrame
    data_html = data_df.to_html()
    if showOutput:
        print('Elements: {}\nColumns: {}\nRows: {}'.format(elements, \
                                                           columns, \
                                                           rows))
        print('Column Names: {}'.format(column_names))
        print('\nPandas DataFrame: ')
        #display(data_df)
        print('\nHTML Generated: \n\n' + data_html)
        
    return (data_html, data_df)

##########################################
### BODY #################################
##########################################

# dict a
# load from file
file = open('db.txt','r')
a = pickle.load(file)
file.close()

# this needs to go into seperate file, where is saves the dict 
# otherwise things a overwritten

#insert('cheese',0)
#insert('bread',5)

#delete('cheese')

# provisory
#a = update(a)

def output():
	print a

	data = to_list(a)

	print data

	#data = ['one','two','three','four','five','six','seven','eight','nine']
	columns = 2                   # Number of Columns
	columns_or_rows = columns
	column_name_prefix = 'Column' # Prefix for Column headers
	span_axis = 1                 # Span along a row (1) or a column (0) first
	showOutput = True            # Use False to suppress printing output

	# Generate HTML
	data_html1, data_df1 = generate_html_with_table(data, columns_or_rows, column_name_prefix, span_axis, showOutput)

	content ="<h1>Stock piling</h1>"+ data_html1 + u"<p> date of today is " + str("{:%B %d, %Y}".format(datetime.now())) +"</p>"
	
	#redmarker = u"<font color="+u"red"+"><b>!-</b></font>"
	contentr = content.replace(u"&lt;",u"<")
	contentr = contentr.replace(u"&gt;",u">")
	contentr = contentr.replace(u"<...",u"")

	# save data html to file
	Html_file= open("piling.html","w")
	Html_file.write(contentr)
	Html_file.close()

	# save data to pickle dump
	# dump to file
	file = open('db.txt','w')
	pickle.dump(a, file)
	file.close()
	
#####################################################
### CHANGE ##########################################
#####################################################

#p('haribo',30)
#pp('haribo')

#####################################################
output()