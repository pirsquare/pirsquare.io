Title: Today, flight search is easier than food search
Author: Ryan Liao
Date: 1st July 2016
FacebookImage: http://pirsquare.io/images/July-2016/best-chicken-rice.png
FacebookDescription: In this post, I will be sharing AudiencePi's tech stack to give others an idea on the fun and challenges in building an adtech product. 

Food search isn't exactly horrible, but it's still far from optimal. It's sad to say that currently, flight search is easier than food search. Ratings system used by existing players like HungryGoWhere (HGW) is fundamentally flawed and it seems that after the founders left the company, HGW hasn't been innovating.

Take a look at search result for "hungrygowhere kfc" on google below.

![search-result](http://pirsquare.io/images/July-2016/search-result.png)

Definitely not a result that I would trust. I'm pretty sure KFC isn't anywhere near perfection.

## Problem ##
**Eatery's outlets as seperate entity**  
HGW's choice of rating eatery by individual outlets rather than rating eatery as a single entity doesn't seem right. One possible unwanted scenario you can get is having several different outlets with ratings that contradicts one another, causing more confusion to users.

For example, given the following results:  
- KFC Punggol, 25% with 4 votes  
- KFC Hougang, 50% with 4 votes  
- KFC Sengkang, 100% with 4 votes  
- KFC Yishun, 0 votes  
- Popeyes Yishun, 65% with 10 votes  

Let's say you stay at Yishun and you would like to have fried chicken for dinner. Now, would you choose KFC or Popeyes? (Okay I know that in real life, it's no-brainer to choose Popeyes).

Another drawback of rating eatery by individual outlets is that it reduces the sample size of eatery's votes, which leads to more bias in search results. It certainly didn't help when HGW are using thumbs up/down methodology for voting, and this explains why most of HGW's results are highly skewed.

**Rating at eatery level**  
The appoarch of rating by eatery doesn't work for every eatery. Using KFC as an illustration. Let's say that you are a big fan of KFC's fried chicken but loathe their burgers and fries. Now, how would you rate KFC? Do you rate it based on your favorite dish or do you rate them based on the average?

Quite simply, the above appoarch only answers questions like "How does KFC food fare?". If you want to find out how specific dishes from KFC fare, you are out of luck.

## Eatasy ##
Few months back, I started working on Eatasy (derived from term "eat tasty") to create a platform that would solve all these pain points that I have experienced with HGW. I want to make food search a more enjoyable experience than flight search.

The considerations mentioned ealier formulates some of key core designs for Eatasy:  
- User shouldn't be rating eatery by individual outlets. Instead, they will rate eatery as single entity.  
- Use a more suitable methodology for food rating. For Eatasy, we allow users to rate between 1 to 10 with 0.5 increment/decrement.  
- Make rating at eatery's dish level a mandatory requirement.
  

*Even though eatery with multiple outlets are group under a single entity, users can still easily find out outlets available for eatery and filter search results by location of outlets.*  

![search-outlets](http://pirsquare.io/images/July-2016/search-outlets.png)


*Finding the best chicken rice in Singapore*  

![best-chicken-rice](http://pirsquare.io/images/July-2016/best-chicken-rice.png)

Okay, enough reading, why not [find something nice to eat](https://eatasy.com/search/).


> Tip: Data and ratings is still lacking but if you trust my recommendations, you can filter by "Editors' Picks".

