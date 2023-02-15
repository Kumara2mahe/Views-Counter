###
<h1 align="center">Views Counter</h1>

<b>Views Counter</b> is badge generator service to count visitors your site/GitHub profiles gets. It counts how many times your site/GitHub profile has been viewed and displays them as a static badge.

<div align="right">  
  <img src="https://views-counter.vercel.app/badge?pageId=Kumara2mahe%2FViews-Counter&leftColor=c0c0c0&rightColor=0080ff&type=daily&label=Today&style=upper" alt="Today">
  &ensp;
  <img src="https://views-counter.vercel.app/badge?pageId=Kumara2mahe%2FViews-Counter&rightColor=0adb3f" alt="Viewers">
</div>
<br>

## Customizing Your Own Views Counter Badge

<br>

> ### Method: 1
To create a counter with all default options, the only required argument is `pageId`, let take it as this repo's path

Markdown
```markdown
![Views Counter](https://views-counter.vercel.app/badge?pageId=Kumara2mahe%2FViews-Counter)
```
HTML
```html
<img src="https://views-counter.vercel.app/badge?pageId=Kumara2mahe%2FViews-Counter" alt="Views Counter">
```
URL
```
https://views-counter.vercel.app/badge?pageId=Kumara2mahe%2FViews-Counter
```
<br>

> **Note** : Don't forget to replace example `Kumara2mahe%2FViews-Counter` with your own value.

<br>

![Views Counter](https://views-counter.vercel.app/badge?pageId=Kumara2mahe%2FViews-Counter)

<br>

### Optional Parameters
- `leftColor` - background color for the text on badge (default is "000" represents black)

- `rightColor` - background color of the count on badge (default is "00F" represents blue)

- `label` - text to be displayed on badge (default is "Visitors")

- `type` - decides how count is displayed, these supported values are

  - "total" (default) : displayed the total views record and it increments when page reloads.
  - "daily" : displayed the total views record only for today and reset every midnight, it also increments when page reloads.
  - "unique" : record only the unique visits based on user IP which increments for every 30 minutes.

- `sessionExpire` - which takes number as minutes to override the unique IP expire duration (default is 30 minutes)

- `style` - shows the text on label as lower or upper case or as entered.
  
  - "upper" : converts the text to uppercase
  - "lower" : converts the text to lowercase
  - "none" (default) : displays the text as it is.

<br>

> **Points To Remember** :
> 1. Every parameters is case-sensitive expert the `leftColor` and `rightColor`. <br>
> 2. For color values only HEX color codes in format "RRGGBB" or "RGB" are valid

<br>

#### Example of Badge with all parameters
```markdown
![Views Counter](https://views-counter.vercel.app/badge?pageId=Kumara2mahe%2FViews-Counter&leftColor=400000&rightColor=ff8080&type=unique&sessionExpire=60&label=Visitors&style=upper)
```
![Views Counter](https://views-counter.vercel.app/badge?pageId=Kumara2mahe%2FViews-Counter&leftColor=400000&rightColor=ff8080&type=unique&sessionExpire=60&label=Visitors&style=upper)

<br>

> **Warning** : While using parameter `type=unique` it get the unique visits by IP. But in Github, there is no way to get the username, browser user agent or IP address of the visitor because GitHub proxies all image URLs through the [GitHub Camo service](https://github.blog/2010-11-13-sidejack-prevention-phase-3-ssl-proxied-assets/). So it won't work for github markups but it works for your personal site or portfolios or blogs. If it doesn't work raise an issue, and I'll look at it as soon as possible!

<br>

## Generating Your Own Views Counter Badge

<br>

> ### Method: 2
- Go to [View-Counter](https://views-counter.vercel.app) website.
- Fill the form with badge `PageId` and other optional parameters as needed.
- Submit form and your badge url, markdown and html are generated automatically.
- Copy the code to the location you want to use it.

<br>

____

### License

- `View-Counter` application is open-sourced software licensed under the [MIT license](LICENSE.md) by [Mahendra Kumara](https://github.com/Kumara2mahe).
