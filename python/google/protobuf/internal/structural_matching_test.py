# Protocol Buffers - Google's data interchange format
# Copyright 2023 Google Inc.  All rights reserved.
# https://developers.google.com/protocol-buffers/
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
#     * Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above
# copyright notice, this list of conditions and the following disclaimer
# in the documentation and/or other materials provided with the
# distribution.
#     * Neither the name of Google Inc. nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""Tests for Py3.10+ structural matching on protobufs."""
from collections.abc import Sequence, Mapping

import unittest


from google.protobuf.internal import structural_matching_example_pb2


class StructuralMatchingTest(unittest.TestCase):

  def test_scalar_match(self) -> None:
    message = structural_matching_example_pb2.TestMessage(
        int_scalar=10,
    )

    actual_match_result: int | None
    match message:
      case structural_matching_example_pb2.TestMessage(int_scalar=5):
        actual_match_result = message.int_scalar
      case structural_matching_example_pb2.TestMessage(int_scalar=10):
        actual_match_result = message.int_scalar
      case _:
        actual_match_result = None

    self.assertEqual(actual_match_result, 10)

  def test_nested_msg_match(self) -> None:
    message = structural_matching_example_pb2.TestMessage(
        nested_msg=structural_matching_example_pb2.TestMessage(int_scalar=10),
    )

    actual_match_result: int | None
    match message:
      case structural_matching_example_pb2.TestMessage(
          nested_msg=structural_matching_example_pb2.TestMessage(int_scalar=5)
      ):
        actual_match_result = message.nested_msg.int_scalar
      case structural_matching_example_pb2.TestMessage(
          nested_msg=structural_matching_example_pb2.TestMessage(int_scalar=10)
      ):
        actual_match_result = message.nested_msg.int_scalar
      case _:
        actual_match_result = None

    self.assertEqual(actual_match_result, 10)

  def test_scalar_sequence_full_match(self) -> None:
    message = structural_matching_example_pb2.TestMessage(
        int_sequence=(1, 2, 3),
    )

    actual_match_result: Sequence[int] | None
    match message:
      case structural_matching_example_pb2.TestMessage(int_sequence=(9, 8, 7)):
        actual_match_result = message.int_sequence
      case structural_matching_example_pb2.TestMessage(int_sequence=(1, 2)):
        actual_match_result = message.int_sequence
      case structural_matching_example_pb2.TestMessage(int_sequence=(1, 2, 3)):
        actual_match_result = message.int_sequence
      case _:
        actual_match_result = None

    self.assertSequenceEqual(actual_match_result, (1, 2, 3))

  def test_scalar_sequence_partial_match(self) -> None:
    message = structural_matching_example_pb2.TestMessage(
        int_sequence=(1, 2, 3),
    )

    actual_match_init: int | None
    actual_match_rest: Sequence[int] | None
    match message:
      case structural_matching_example_pb2.TestMessage(int_sequence=(9, *rest)):
        actual_match_init = 9
        actual_match_rest = rest
      case structural_matching_example_pb2.TestMessage(int_sequence=(1, *rest)):
        actual_match_init = 1
        actual_match_rest = rest
      case _:
        actual_match_init = None
        actual_match_rest = None

    self.assertEqual(actual_match_init, 1)
    self.assertSequenceEqual(actual_match_rest, (2, 3))

  def test_msg_sequence_full_match(self) -> None:
    message = structural_matching_example_pb2.TestMessage(
        msg_sequence=(
            structural_matching_example_pb2.TestMessage(int_scalar=1),
            structural_matching_example_pb2.TestMessage(int_scalar=2),
            structural_matching_example_pb2.TestMessage(int_scalar=3),
        )
    )

    actual_match_result: Sequence[
        structural_matching_example_pb2.TestMessage
    ] | None
    match message:
      case structural_matching_example_pb2.TestMessage(
          msg_sequence=(
              structural_matching_example_pb2.TestMessage(int_scalar=9),
              structural_matching_example_pb2.TestMessage(int_scalar=8),
              structural_matching_example_pb2.TestMessage(int_scalar=7),
          )
      ):
        actual_match_result = (9, 8, 7)
      case structural_matching_example_pb2.TestMessage(
          msg_sequence=(
              structural_matching_example_pb2.TestMessage(int_scalar=1),
              structural_matching_example_pb2.TestMessage(int_scalar=2),
          )
      ):
        actual_match_result = (1, 2)
      case structural_matching_example_pb2.TestMessage(
          msg_sequence=(
              structural_matching_example_pb2.TestMessage(int_scalar=1),
              structural_matching_example_pb2.TestMessage(int_scalar=2),
              structural_matching_example_pb2.TestMessage(int_scalar=3),
          )
      ):
        actual_match_result = (1, 2, 3)
      case _:
        actual_match_result = None

    self.assertSequenceEqual(actual_match_result, (1, 2, 3))

  def test_msg_sequence_partial_match(self) -> None:
    message = structural_matching_example_pb2.TestMessage(
        msg_sequence=(
            structural_matching_example_pb2.TestMessage(int_scalar=1),
            structural_matching_example_pb2.TestMessage(int_scalar=2),
            structural_matching_example_pb2.TestMessage(int_scalar=3),
        )
    )

    actual_match_init: int | None
    actual_match_rest: Sequence[
        structural_matching_example_pb2.TestMessage
    ] | None
    match message:
      case structural_matching_example_pb2.TestMessage(
          msg_sequence=(
              structural_matching_example_pb2.TestMessage(int_scalar=9),
              *rest,
          )
      ):
        actual_match_init = 9
        actual_match_rest = rest
      case structural_matching_example_pb2.TestMessage(
          msg_sequence=(
              structural_matching_example_pb2.TestMessage(int_scalar=1),
              *rest,
          )
      ):
        actual_match_init = 1
        actual_match_rest = rest
      case _:
        actual_match_init = None
        actual_match_rest = None

    self.assertEqual(actual_match_init, 1)
    self.assertSequenceEqual(
        actual_match_rest,
        (
            structural_matching_example_pb2.TestMessage(int_scalar=2),
            structural_matching_example_pb2.TestMessage(int_scalar=3),
        ),
    )

  def test_mapping_full_match(self) -> None:
    message = structural_matching_example_pb2.TestMessage(
        string_to_msg={
            "one": structural_matching_example_pb2.TestMessage(int_scalar=1),
            "two": structural_matching_example_pb2.TestMessage(int_scalar=2),
        },
    )

    actual_result: Mapping[str, int] | None
    match message:
      case structural_matching_example_pb2.TestMessage(
          string_to_msg={
              "one": structural_matching_example_pb2.TestMessage(int_scalar=2),
              "two": structural_matching_example_pb2.TestMessage(int_scalar=2),
          }
      ):
        actual_result = {"one": 2, "two": 2}
      case structural_matching_example_pb2.TestMessage(
          string_to_msg={
              "one": structural_matching_example_pb2.TestMessage(int_scalar=1),
              "two": structural_matching_example_pb2.TestMessage(int_scalar=2),
          },
      ):
        actual_result = {"one": 1, "two": 2}
      case _:
        actual_result = None

    self.assertDictEqual(actual_result, {"one": 1, "two": 2})

  def test_mapping_partial_match(self) -> None:
    message = structural_matching_example_pb2.TestMessage(
        string_to_msg={
            "one": structural_matching_example_pb2.TestMessage(int_scalar=1),
            "two": structural_matching_example_pb2.TestMessage(int_scalar=2),
            "three": structural_matching_example_pb2.TestMessage(int_scalar=3),
        },
    )

    actual_one_value_match: str | None
    actual_rest_match: Mapping[
        str, structural_matching_example_pb2.TestMessage
    ] | None
    match message:
      case structural_matching_example_pb2.TestMessage(
          string_to_msg={
              "two": structural_matching_example_pb2.TestMessage(int_scalar=1),
              **rest,
          }
      ):
        actual_one_value_match = 1
        actual_rest_match = rest
      case structural_matching_example_pb2.TestMessage(
          string_to_msg={
              "two": structural_matching_example_pb2.TestMessage(int_scalar=2),
              **rest,
          }
      ):
        actual_one_value_match = 2
        actual_rest_match = rest
      case _:
        actual_one_value_match = None
        actual_rest_match = None

    self.assertEqual(actual_one_value_match, 2)
    self.assertDictEqual(
        actual_rest_match,
        {
            "one": structural_matching_example_pb2.TestMessage(int_scalar=1),
            "three": structural_matching_example_pb2.TestMessage(int_scalar=3),
        },
    )

  def test_oneof_variable_match_unguarded(self) -> None:
    message = structural_matching_example_pb2.TestMessage(
        a=structural_matching_example_pb2.TestA(value="TestA")
    )

    # This is surprising, but expected: message.b will be the empty default
    # message, which in turn will yield an empty string as default value.
    actual_match: str | None
    match message:
      case structural_matching_example_pb2.TestMessage(
          b=structural_matching_example_pb2.TestB(value=matched_value)
      ):
        actual_match = matched_value
      case _:
        actual_match = None

    self.assertEqual(actual_match, "")

  def test_oneof_variable_match_guarded(self) -> None:
    message = structural_matching_example_pb2.TestMessage(
        a=structural_matching_example_pb2.TestA(value="TestA")
    )

    actual_match: str | None
    match message:
      case structural_matching_example_pb2.TestMessage(
          b=structural_matching_example_pb2.TestB(value=matched_value)
      ) if matched_value:
        actual_match = matched_value
      case structural_matching_example_pb2.TestMessage(
          a=structural_matching_example_pb2.TestA(value=matched_value)
      ) if matched_value:
        actual_match = matched_value
      case _:
        actual_match = None

    self.assertEqual(actual_match, "TestA")

if __name__ == "__main__":
  unittest.main()
