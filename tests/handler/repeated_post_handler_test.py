import unittest
from datetime import datetime
from unittest.mock import MagicMock

from plemmy import LemmyHttp

from lemmypostbot import RepeatedPost, RepeatedPostHandler, PostTemplate, PostContext
from lemmypostbot.handler.handler import ScheduledCallback
from lemmypostbot.handler.repeated_post_handler import CreatePostTask, PostUnpinTask


class TestRepeatedPostHandler(unittest.TestCase):

    def test_get_next(self):
        # Mock the RepeatedPost object
        config = RepeatedPost(
            period='*/5 * * * *',
            only_first_of_month=False,
            post=PostTemplate(
                ""
            ),
            context=PostContext(
                "trans"
            )
        )

        # Get the next scheduled callback
        scheduled_callback = RepeatedPostHandler.get_next(config)

        # Assert that the scheduled callback is of type ScheduledCallback
        self.assertIsInstance(scheduled_callback, ScheduledCallback)

    def test_can_handle(self):
        handler = RepeatedPostHandler()

        # Test with a RepeatedPost object
        config = RepeatedPost(
            period='*/5 * * * *',
            only_first_of_month=False,
            post=PostTemplate(
                ""
            ),
            context=PostContext(
                "trans"
            )
        )
        self.assertTrue(handler.can_handle(config))

        # Test with a non-RepeatedPost object
        self.assertFalse(handler.can_handle({}))

    def test_initial(self):
        handler = RepeatedPostHandler()

        # Mock the RepeatedPost object
        config = RepeatedPost(
            period='*/5 * * * *',
            only_first_of_month=False,
            post=PostTemplate(
                ""
            ),
            context=PostContext(
                "trans"
            )
        )

        # Get the initial scheduled callbacks
        scheduled_callbacks = handler.initial(config)

        # Assert that the scheduled callbacks list is not empty
        self.assertNotEqual(len(scheduled_callbacks), 0)


class TestCreatePostTask(unittest.TestCase):

    def test_handle(self):
        # Mock the RepeatedPost object
        config = RepeatedPost(
            period='*/5 * * * *',
            only_first_of_month=False,
            post=PostTemplate(
                ""
            ),
            context=PostContext(
                "trans"
            )
        )

        # Mock the LemmyHttp object
        request = MagicMock(spec=LemmyHttp)

        # Create the CreatePostTask instance
        task = CreatePostTask(config)

        # Call the handle method and assert the return value
        scheduled_callbacks = task.handle(request)
        self.assertIsInstance(scheduled_callbacks, list)

    def test_first_occurrence_in_month(self):
        # Mock the RepeatedPost object
        config = RepeatedPost(
            period='0 0 1 * *',
            only_first_of_month=True,
            post=PostTemplate(
                ""
            ),
            context=PostContext(
                "trans"
            )
        )

        current_date = datetime(year=2024, month=5, day=1)

        # Create the CreatePostTask instance
        task = CreatePostTask(config)

        # Call the _first_occurrence_in_month method
        result = task._first_occurrence_in_month(current_date)

        # Assert that the result is True since today is the first of the month
        self.assertTrue(result)

        current_date = datetime(year=2024, month=5, day=15)
        result = task._first_occurrence_in_month(current_date)
        self.assertFalse(result)

    def test_first_occurrence_in_month_weekday(self):
        # Mock the RepeatedPost object
        config = RepeatedPost(
            period='0 0 * * FRI',
            only_first_of_month=True,
            post=PostTemplate(
                ""
            ),
            context=PostContext(
                "trans"
            )
        )

        current_date = datetime(year=2024, month=5, day=3)

        # Create the CreatePostTask instance
        task = CreatePostTask(config)

        # Call the _first_occurrence_in_month method
        result = task._first_occurrence_in_month(current_date)

        # Assert that the result is True since today is the first of the month
        self.assertTrue(result)

        current_date = datetime(year=2024, month=5, day=10)
        result = task._first_occurrence_in_month(current_date)
        self.assertFalse(result)


class TestPostUnpinTask(unittest.TestCase):

    def test_handle(self):
        # Mock the post_id
        post_id = 123

        # Mock the LemmyHttp object
        request = MagicMock(spec=LemmyHttp)

        # Create the PostUnpinTask instance
        task = PostUnpinTask(post_id)

        # Call the handle method and assert the return value
        scheduled_callbacks = task.handle(request)
        self.assertIsInstance(scheduled_callbacks, list)