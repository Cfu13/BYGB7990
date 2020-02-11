from selenium import webdriver

# str(input("Enter the movie you want to parse(for example joker_2019): "))
# int(input("Enter pages you want to parse(for first 3 pages, enter 3): "))
movie = 'joker_2019'
pageNum = 30

browser = webdriver.Chrome("/Users/chong/chromedriver")
browser.implicitly_wait(10)

url = str("https://rottentomatoes.com/m/" + movie + "/reviews?page=1")

with open('/Users/Chong/chongdi_fu_movie.txt', 'w', encoding='utf8') as mv:
    for page in range(1, pageNum + 1):
        browser.get(url)  # go to the page

        reviews = browser.find_elements_by_css_selector("[class*=review_table]")

        tst = ()  # to test if review repeated

        for review in reviews:
            name, rating, source, text, date = 'NA', 'NA', 'NA', 'NA', 'NA'

            # I found selenium will parse the first reviews twice, need to avoid duplication
            try:
                name = review.find_element_by_css_selector("a.unstyled.bold.articleLink").text
                # check if name repeated
                if tst == name:
                    continue
                else:
                    tst = name
            except:
                print('no name')

            # locate the icon and take the attribute name out
            try:
                rating = review.find_element_by_css_selector("div.review_icon.icon.small") \
                    .get_attribute('class')
            except:
                print('no rating')
            if rating == 'review_icon icon small rotten':
                rating = "rotten"
            elif rating == 'review_icon icon small fresh':
                rating = "fresh"
            # well...I don't think there exists any other possible rating...
            # but anyway...
            elif rating == '':
                rating = 'NA'

            # get the source
            try:
                source = review.find_element_by_css_selector("em.subtle.critic-publication").text
                if source == '':
                    source = 'NA'
                    print('no source')
                # in case there exist the tags with no content in between, hence no error
            except:
                print('no source')

            # get the review text
            try:
                text = review.find_element_by_css_selector('div.the_review').text
                if text == '':
                    text = 'NA'
                    print('no text')
                # there exist the tags with no content in between, hence no error
            except:
                print('no text')

            # get the date
            try:
                date = review.find_element_by_css_selector('div.review-date.subtle.small').text
                if date == '':
                    date = 'NA'
                    print('no date')
                # there exist the tags with no content in between, hence no error
            except:
                print('no date')

            # write what this loop get in txt file
            mv.write(str(name)
                     + '\t' + str(rating)
                     + '\t' + str(source)
                     + '\t' + text.replace('\n', ' ')
                     + '\t' + str(date)
                     + '\n')

        # stop click when reach the page
        if page == pageNum:
            break

        pageInfo = browser.find_elements_by_css_selector('span.pageInfo')
        for value in pageInfo:
            PAGE = value.text  # here page = 'x of page y' and I need 'y' to indicate max page number
            maxPage = int(PAGE[-2:])  # no movie has reviews more than 100 pages so last 2 characters are enough
        if page == maxPage:
            break

        try:
            # go to next page
            browser.find_element_by_xpath('//*[@id="content"]/div/div/div/div[1]/a[2]').click()
        except:
            # selenium cannot find element due to certain advertisement and pop-ups
            browser.refresh()
            browser.find_element_by_xpath('//*[@id="content"]/div/div/div/div[1]/a[2]').click()
        url = browser.current_url

browser.close()
browser.quit()
