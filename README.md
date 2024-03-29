# HackerNews Digest

This script makes use of GitHub actions to send daily newsletters with the top 10 posts from HackerNews of the previous day.

# How to use it?
- If you are interested to subscribe to the newsletter, you will have to run the cron yourself.
- All you have to do is [fork](https://docs.github.com/en/github/getting-started-with-github/quickstart/fork-a-repo) this repository, and set a few secrets.
- Add the following [secrets](https://docs.github.com/en/actions/reference/encrypted-secrets#creating-encrypted-secrets-for-a-repository) in your forked repository :
  - `SMTP_HOST` - This is the domain of SMTP server (Eg: smtp.gmail.com or smtp.mail.me.com)
  - `SMTP_FROM` - This is the email address that will be used to send the newsletters.
  - `SMTP_PASS` - This is the password for the `SMTP_FROM` email address.
  - `SMTP_TO` - This is the email address of the recipient. Most often, this will be the same as `SMTP_FROM`.
- Once the above steps are done, you will start receiving emails in the `SMTP_TO` address every day at 07:30 AM.

# How does it look?

![image](screenshot.png)