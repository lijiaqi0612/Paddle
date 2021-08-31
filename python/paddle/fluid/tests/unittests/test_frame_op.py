# Copyright (c) 2021 PaddlePaddle Authors. All Rights Reserved.
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import librosa
import numpy as np
import paddle
import unittest

from op_test import OpTest


class TestFrameOp(OpTest):
    def setUp(self):
        self.op_type = "frame"
        self.shape, self.type, self.attrs = self.initTestCase()
        self.inputs = {
            'X': np.random.random(size=self.shape).astype(self.type),
        }
        self.outputs = {
            'Out': librosa.util.frame(
                x=self.inputs['X'], **self.attrs)
        }

    def initTestCase(self):
        input_shape = (150, )
        input_type = 'float64'
        attrs = {
            'frame_length': 50,
            'hop_length': 15,
            'axis': -1,
        }
        return input_shape, input_type, attrs

    def test_check_output(self):
        paddle.enable_static()
        self.check_output()
        paddle.disable_static()

    def test_check_grad_normal(self):
        paddle.enable_static()
        self.check_grad(['X'], 'Out')
        paddle.disable_static()


class TestCase1(TestFrameOp):
    def initTestCase(self):
        input_shape = (150, )
        input_type = 'float64'
        attrs = {
            'frame_length': 50,
            'hop_length': 15,
            'axis': 0,
        }
        return input_shape, input_type, attrs


class TestCase2(TestFrameOp):
    def initTestCase(self):
        input_shape = (8, 150)
        input_type = 'float64'
        attrs = {
            'frame_length': 50,
            'hop_length': 15,
            'axis': -1,
        }
        return input_shape, input_type, attrs


class TestCase3(TestFrameOp):
    def initTestCase(self):
        input_shape = (150, 8)
        input_type = 'float64'
        attrs = {
            'frame_length': 50,
            'hop_length': 15,
            'axis': 0,
        }
        return input_shape, input_type, attrs


# FIXME(chenxiaojie06): There are bugs when input dims >= 3 in librosa.
# class TestCase3(TestFrameOp):
#     def initTestCase(self):
#         input_shape = (4, 2, 150)
#         input_type = 'int32'
#         attrs = {
#             'frame_length': 50,
#             'hop_length': 15,
#             'axis': -1,
#         }
#         return input_shape, input_type, attrs

# class TestCase4(TestFrameOp):
#     def initTestCase(self):
#         input_shape = (150, 4, 2)
#         input_type = 'int32'
#         attrs = {
#             'frame_length': 50,
#             'hop_length': 15,
#             'axis': 0,
#         }
#         return input_shape, input_type, attrs

if __name__ == '__main__':
    unittest.main()
