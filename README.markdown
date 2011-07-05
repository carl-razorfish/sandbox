My Sandbox
=========

Installation Information
------------------------

1. Install [Sass](http://sass-lang.com/tutorial)
2. In your terminal, move into the project directory `cd <project>`
3. Run the command : `sass --watch src/scss:static/css`

Request Handlers
----------------

There are 2 request handlers, Mashup and RestAPI.

### 1. Mashup

- Accepts any context path as the single HTTP GET Request argument
- Subsequent work will then attempt to generate feed data based on that context path
- Examples:
	- ROOT_APP/newyork

### 2. RestAPI

- Accepts any context path as argument #1 in the HTTP GET Request context path
- Accepts only the following two valid values as #2 argument in the HTTP GET Request context path
    - xml
	- json
- Subsequent work will then attempt to generate feed data based on that context path and response data format 
- Examples:
	- ROOT_APP/newyork/xml [valid]
	- ROOT_APP/newyork/json [valid]
	- ROOT_APP/newyork/blah [invalid, will default to Mashup request handler]