# Static Site Generator

import os
from datetime import datetime
from jinja2 import Environment, PackageLoader
from markdown2 import markdown

POSTS = {}

for md_post in os.listdir('content'):
	path = os.path.join('content', md_post)
	
	with open(path, 'r') as content:
		POSTS[md_post] = markdown(content.read(), extras=['metadata'])

	POSTS = {
		post: POSTS[post] for post in sorted(POSTS, key=lambda post: datetime.strptime(POSTS[post].metadata['date'], '%Y%d%m'), reverse=True)
	}

	env = Environment(loader=PackageLoader('ssg', 'templates'))
	index = env.get_template('index.html')
	post_template = env.get_template('post-detail.html')
	
	post_meta = [POSTS[post].metadata for post in POSTS]
	index_content = index.render(posts=post_meta)
	
	with open('output/index.html', 'w') as output:
		output.write(index_content)
		
for post in POSTS:
	post_meta = POSTS[post].metadata
	
	post_data = {
		'content': POSTS[post],
		'title': post_meta['title'],
		'date': post_meta['date']
	}
	
	post_content = post_template.render(post=post_data)
	
	post_path = 'output/posts/{slug}/index.html'.format(slug=post_meta['slug'])
	
	os.makedirs(os.path.dirname(post_path), exist_ok=True)
	with open(post_path, 'w') as post:
		post.write(post_content)
