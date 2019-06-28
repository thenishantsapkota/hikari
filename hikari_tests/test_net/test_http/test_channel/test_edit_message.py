#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright © Nekoka.tt 2019
#
# This file is part of Hikari.
#
# Hikari is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Hikari is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Hikari. If not, see <https://www.gnu.org/licenses/>.

import asynctest
import pytest


@pytest.fixture()
async def http_client(event_loop):
    from hikari_tests.test_net.test_http import ClientMock

    return ClientMock(token="foobarsecret", loop=event_loop)


@pytest.mark.asyncio
async def test_no_changes(http_client):
    # not sure if this is even valid, TODO: verify this
    http_client.request = asynctest.CoroutineMock()
    await http_client.edit_message("123456", "6789012")
    http_client.request.assert_awaited_once_with(
        "patch", "/channels/{channel_id}/messages/{message_id}", channel_id="123456", message_id="6789012", json={}
    )


@pytest.mark.asyncio
async def test_edit_content(http_client):
    http_client.request = asynctest.CoroutineMock()
    await http_client.edit_message("123456", "6789012", content="ayy lmao im a duck")
    http_client.request.assert_awaited_once_with(
        "patch",
        "/channels/{channel_id}/messages/{message_id}",
        channel_id="123456",
        message_id="6789012",
        json={"content": "ayy lmao im a duck"},
    )


@pytest.mark.asyncio
async def test_edit_embed(http_client):
    http_client.request = asynctest.CoroutineMock()
    await http_client.edit_message("123456", "6789012", embed={"title": "ayy lmao im a duck"})
    http_client.request.assert_awaited_once_with(
        "patch",
        "/channels/{channel_id}/messages/{message_id}",
        channel_id="123456",
        message_id="6789012",
        json={"embed": {"title": "ayy lmao im a duck"}},
    )


@pytest.mark.asyncio
async def test_edit_embed_and_content(http_client):
    http_client.request = asynctest.CoroutineMock()
    await http_client.edit_message("123456", "6789012", embed={"title": "ayy lmao im a duck"}, content="quack")
    http_client.request.assert_awaited_once_with(
        "patch",
        "/channels/{channel_id}/messages/{message_id}",
        channel_id="123456",
        message_id="6789012",
        json={"embed": {"title": "ayy lmao im a duck"}, "content": "quack"},
    )


@pytest.mark.asyncio
async def test_return_value(http_client):
    http_client.request = asynctest.CoroutineMock(return_value={"...": "..."})
    result = await http_client.edit_message("123456", "6789012", embed={"title": "ayy lmao im a duck"}, content="quack")
    http_client.request.assert_awaited_once_with(
        "patch",
        "/channels/{channel_id}/messages/{message_id}",
        channel_id="123456",
        message_id="6789012",
        json={"embed": {"title": "ayy lmao im a duck"}, "content": "quack"},
    )
    assert result == {"...": "..."}