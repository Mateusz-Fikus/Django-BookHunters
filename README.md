# BookHunters project

### I did not focus on the design or overall presentation of the website, therefore it looks how it looks.

## How does it work?

User is registering via email, then he needs to activate his account by verification mail (not avaliable in preview version) which includes encoded ID and token.

Then, user is browsing books (added by another users) and when he is interested in purchasing a book, he sends a purchase request to the owner with a message
(all pending requests are avaliable in management panel of specific user, also user can cancel specific request in his management panel).

The seller checks pending request for specific book, reads a message and then selects person whom he would like to send the book to.
When request is accepted, email is being sent to the buyer with offer URL.

## Main features

- Email verifications
- Offer management (edit, update, delete)
- Requests management
- Login
- Register
- Filter
- Initial AWS S3 config

*Project after deployment tests.*

### This is my first django project, therefore I've used function based views instead of class based views. So the code is not really DRY.
The main idea was to focus on most important django functions and its abilities. The project was very worth doing, because I've learned a lot.



