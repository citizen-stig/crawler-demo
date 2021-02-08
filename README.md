# Web crawler demo

# How to start

# Functional Requirements

- implement recursive web-crawler of the site.
- crawler is command-line tool which accept starting url and destination directory
- crawler download the initial url and look to links inside original document (recursively)
- crawler does not walk to link outside initial url (if starting link is https://start.url/abc, then it goes to https://start.url/abc/123 and https://start.url/abc/456, but skip https://another.domain/ and https://start.url/def)
- crawler should correctly process Ctrl+C hotkey
- crawler should be parallel
- crawler should supports continue to load if destination directory already has loaded data (if we cancel download and than continue)


