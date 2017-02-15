# Contact
<form id="contact" name="contactform" method="post" action="/contact">
  <label for="name">
    <h3>Name:</h3>
  </label>
  <input type="text" name="name" placeholder="Name"><br />
  <label for="email">
    <h3>Email Address:</h3>
  </label>
  <input type="email" name="email" required placeholder="you@example.com"><br />
  <label for="subject">
    <h3>Subject:</h3>
  </label>
  <input type="text" name="subject" placeholder="subject"><br />
  <label for="message" style="vertical-align:top;">
    <h3>Message:</h3>
  </label>
  <textarea name="message" required id="message" rows="15" cols="40"></textarea><br />
  <input type="submit" value="Submit">
</form>
