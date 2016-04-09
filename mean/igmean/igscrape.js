var InstagramPosts, streamOfPosts;
InstagramPosts = require('instagram-screen-scrape');
 
streamOfPosts = new InstagramPosts({
  username: 'imbrettdalton'
});
 
streamOfPosts.on('readable', function() {
  var post, time;
  post = streamOfPosts.read();
  time = new Date(post.time * 1000);
  console.log([
    "slang800's post from ",
    time.toLocaleDateString(),
    " got ",
    post.like,
    " like(s), and ",
    post.comment,
    " comment(s)"
  ].join(''));
});