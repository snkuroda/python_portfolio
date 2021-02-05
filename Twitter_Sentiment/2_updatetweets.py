"""
 parse coords columns into x and y coords

 Extract old table as RAW table
 cursor -> fetch -> parse coods (and html from text) -> re-upload  
 create new table (Revised) 
"""
import sqlite3, dataset, re, fnmatch
table_list = ['trump', 'climate', 'news', 'politics', 'covfefe']

for inTable in table_list:

    db = dataset.connect("sqlite:///selected_tweets.db")
    conn = sqlite3.connect("tweetstest.db")
    curs = conn.cursor()
    curs.execute("SELECT * FROM %s" % inTable).fetchone()
    outTable = inTable
    ### Extract data and parse tweets out

    for row in curs:
        id_str = row[1]
        x_coords = eval(row[2])["coordinates"][1]
        y_coords = eval(row[2])["coordinates"][0]
        user = row[3]
        sentiment = row[4]

        tweet_list = [id_str, user, x_coords, y_coords, sentiment]
        
        #Checks for presence of weblink and then pull Website out of text if there is.
        raw_text = row[5]
        
        https = r"https:"
        http = r"http:"
        # Determines if weblink is present
        link_number = 1
        
        #Parses tweets if the contains a https link (majority)
        if raw_text.count(https) > 0:
            while link_number != 0 :
                web_present = True
                webLinks = []
                tweet_list.append(web_present)
                # Splits the text up and searches for weblink       
                text_list = raw_text.split(" ")
                wild = fnmatch.filter(text_list, '*%s*' %https)
                link_number = len(wild)

                # Iterates through tweets and pulls out web links and puts tweet together again
                for link in wild:
                    web_index = text_list.index(link)
                    web_link = text_list.pop(web_index)
                    clean_text = " ".join(text_list)
        
                    
                    webLinks.append(web_link)
                    link_number = link_number - 1
                
                tweet_list.append(clean_text)
                
                webLink1 = webLinks[0]
                tweet_list.append(webLink1)
            if len(webLinks) > 1:
                webLink2 = webLinks[1]
                tweet_list.append(webLink2)
            else:
                webLink2 = "N/A"
                tweet_list.append(webLink2)    
            
        # Parses tweet if the tweet contains a http link
        elif raw_text.count(http) > 0:        
            while link_number != 0:
                web_present = True
                tweet_list.append(web_present)
                webLinks = []

                
                text_list = raw_text.split(" ")
                wild = fnmatch.filter(text_list, '*%s*' %http)
                link_number = len(wild)
                for link in wild:
                    web_index = text_list.index(link)
                    web_link = text_list.pop(web_index)
                    clean_text = " ".join(text_list)
                        
                    webLinks.append(web_link)
                    link_number = link_number - 1

                    final_text = clean_text 
                    tweet_list.append(final_text)
                
                webLink1 = webLinks[0]
                tweet_list.append(webLink1)
            if len(webLinks) > 1:
                webLink2 = webLinks[1]
                tweet_list.append(webLink2)
            else:
                webLink2 = "N/A"
                tweet_list.append(webLink2)    
                 
         
                

        # Does not parse tweet, does not contain a web link
        else:
            web_present = False
            final_text = raw_text
            webLink1 = "N/A"
            webLink2 = "N/A"
            
            tweet_list.append(web_present)
            tweet_list.append(final_text)
            tweet_list.append(webLink1)
            tweet_list.append(webLink2)
            

        
        # Insert into a SQLite Table    
        table = db["%s" % outTable]
        table.insert(dict(
            tweet_id = tweet_list[0],
            user_name = tweet_list[1],
            x_coordinate = tweet_list[2],
            y_coordinate = tweet_list[3],
            tweet = tweet_list[6],
            sentiment_score = tweet_list[4],
            web_link_present = tweet_list[5],
            web_link1 = tweet_list[7],
            web_link2 = tweet_list[8]))

        print("tweet added", tweet_list[6])
    print(inTable + " tweets done")
        
