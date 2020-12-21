import pytest
from src.ytom import *


@pytest.mark.parametrize("url,expected", [
    ('https://www.youtube.com/watch?v=ASKPfSQvdnM', True),
    ('https://youtu.be/ASKPfSQvdnM', True),
    ('https://www.youtube.com/watch?v=ASKPfSQvdnMhttps://www.youtube.com/watch?v=ASKPfSQvdnM', True),
    ('https://www.youtube.com/watchSKPfSQvdnM', False),
    ('https://www.youtm/watch?v=ASKPfSQvdnM', False),
    ('htom/watch?v=ASKPfSQvdnM', False),
    ('https://www.dailymotion.com/video/x2ixmnj', False),
    ('1234', False),
    ('', False),
    (' ', False),
])
def test_is_youtube_url(url, expected):
    assert is_youtube_url(url) == expected


@pytest.mark.parametrize("url,expected", [
    ('https://www.youtube.com/watch?v=ASKPfSQvdnM', 'ASKPfSQvdnM'),
    ('https://youtu.be/ASKPfSQvdnM', 'ASKPfSQvdnM'),
    ('https://www.youtube.com/watch?v=ASKPfSQvdnMhttps://www.youtube.com/watch?v=ASKPfSQvdnM', 'ASKPfSQvdnM'),
    ('https://www.dailymotion.com/video/x2ixmnj', ''),
    ('12345', ''),
    (' ', ''),
    ('', ''),

])
def test_get_video_id_from_youtube_url(url, expected):
    assert get_video_id_from_youtube_url(url) == expected
