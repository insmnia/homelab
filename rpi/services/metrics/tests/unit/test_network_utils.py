import pytest
from app.core.network_utils import get_self_ip
from unittest.mock import MagicMock


def test_get_self_ip_caching(mock_subprocess: MagicMock):
    # arrange
    get_self_ip.cache_clear()
    mock_subprocess.return_value = "192.168.1.1 192.168.1.2\n"

    # act
    result1 = get_self_ip()
    result2 = get_self_ip()  # This should use the cache

    # assert
    assert result1 == "192.168.1.1"
    assert result2 == "192.168.1.1"  # Should be the same result without calling subprocess again
    assert mock_subprocess.call_count == 1, "Subprocess should only be called once due to caching"


def test_get_self_ip_multiple_ips(mock_subprocess: MagicMock):
    # arrange
    get_self_ip.cache_clear()
    mock_subprocess.return_value = "192.168.1.1 192.168.1.2\n"

    # act
    result = get_self_ip()

    # assert
    assert result == "192.168.1.1", "Should return the first IP when multiple are present"


def test_get_self_ip_no_ips(mock_subprocess: MagicMock):
    # arrange
    mock_subprocess.return_value = None
    get_self_ip.cache_clear()

    # act & assert
    with pytest.raises(RuntimeError, match="Couldn't get self ip"):
        get_self_ip()
