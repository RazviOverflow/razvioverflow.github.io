#!/usr/bin/env python

'''
Razvi Son eptember 2018
Contact: Twitter @Razvieu

This script creates tags for your Jekyll blog hosted by Github page.
No plugins required. If you want to use it, make sure you edit post_dirs
to fit your needs.
'''

import glob
import os

post_dirs = ['./','./_microcorruption/']
tag_dir = './tags/'
total_tags = []

# Checking dir existence
if not os.path.exists(tag_dir):
    os.makedirs(tag_dir)

# Deleting old tags
old_tags = glob.glob(tag_dir + '*.md')
for tag in old_tags:
    os.remove(tag)

for post_dir in post_dirs:
    filenames = glob.glob(post_dir + '*md')
    for filename in filenames:
        f = open(filename, 'r')
        crawl = False
        for line in f:
            if crawl:
                #current_tags = line.strip().split()
                if line.startswith("tags:"):
                    auxTags = line.replace("tags:", "")
                    auxTagsBrackets = auxTags.replace("[", "").replace("]", "")
                    myTags = auxTagsBrackets.strip().split(", ")
                    total_tags.extend(myTags[:])
                    crawl = False
                    break
            if line.strip() == '---':
                if not crawl:
                    crawl = True
                else:
                    crawl = False
                    break
        f.close()

total_tags = set(total_tags)

for tag in total_tags:
    tag_filename = tag_dir + tag + '.md'
    f = open(tag_filename, 'a')
    write_str = '---\nlayout: tagpage\ntitle: \"Tag: ' + tag + '\"\ntag: ' + tag + '\nrobots: noindex\n---\n'
    f.write(write_str)
    f.close()

print("A total of ", total_tags.__len__(), " tags have been generated.\nThe generated tags are: ")
print(*list(total_tags), sep=", ")