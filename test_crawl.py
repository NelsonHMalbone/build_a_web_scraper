import unittest
from crawl import normalize_url
from main import get_heading_from_html, get_first_paragraph_from_html,get_urls_from_html,get_images_from_html


class TestCrawl(unittest.TestCase):

    def test_normalize_url(self):
        input_url = "https://www.boot.dev/blog/path"
        actual = normalize_url(input_url)
        expected = "www.boot.dev/blog/path"
        self.assertEqual(actual, expected)

    # h1 heading test
    def test_get_heading_from_html_basic(self):
        input_body = "<html><body><h1>Test Title</h1></body></html>"
        actual = get_heading_from_html(input_body)
        expected = "Test Title"
        self.assertEqual(actual, expected)

    def test_get_heading_from_html_basic_h2(self):
        input_body = "<html><body><h2>Test Title</h2></body></html>"
        actual = get_heading_from_html(input_body)
        expected = "Test Title"
        self.assertEqual(actual, expected)

    # p paragraph test
    def test_get_first_paragraph_from_html_main_priority(self):
        input_body = """<html><body>
            <p>Outside paragraph.</p>
            <main>
                <p>Main paragraph.</p>
            </main>
        </body></html>"""
        actual = get_first_paragraph_from_html(input_body)
        expected = "Main paragraph."
        self.assertEqual(actual, expected)

    def test_get_urls_from_html_absolute(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><a href="https://crawler-test.com"><span>Boot.dev</span></a></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://crawler-test.com"]
        self.assertEqual(actual, expected)

    def test_get_urls_from_html_absolute_one(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><a href="/one">One</a></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://crawler-test.com/one"]
        self.assertEqual(actual, expected)

    def test_get_urls_from_html_absolute_two_three(self):
        input_url = "https://crawler-test.com"
        input_body = ('<html><body><a href="https://crawler-test.com/two">Two</a>'
                      '<a href="https://crawler-test.com/three">Three</a></body></html>')
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://crawler-test.com/two", "https://crawler-test.com/three"]
        self.assertEqual(actual, expected)

    def test_get_images_from_html_relative(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><img src="/logo.png" alt="Logo"></body></html>'
        actual = get_images_from_html(input_body, input_url)
        expected = ["https://crawler-test.com/logo.png"]
        self.assertEqual(actual, expected)

    def test_get_images_from_html_relative_one(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><img src="/logo.jpg" alt="Logo"></body></html>'
        actual = get_images_from_html(input_body, input_url)
        expected = ["https://crawler-test.com/logo.jpg"]
        self.assertEqual(actual, expected)

    def test_get_images_from_html_relative_two(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><img alt="Logo"></body></html>'
        actual = get_images_from_html(input_body, input_url)
        expected = []
        self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()