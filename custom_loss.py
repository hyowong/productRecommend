# -*- coding: utf_8 -*-

import tensorflow as tf
import math


def ArcFaceloss(labels, features):
    """
    ArcFace loss function
    """

    N = tf.shape(labels)[0]
    s = 64.
    m = 0.5
    cos_t = features
    cos_m = math.cos(m)
    sin_m = math.sin(m)
    mm = sin_m * m
    threshold = math.cos(math.pi - m)

    cos_t2 = tf.square(features, name='cos_2')
    sin_t2 = tf.subtract(1., cos_t2, name='sin_2')
    sin_t = tf.sqrt(sin_t2, name='sin_t')
    cos_mt = s * tf.subtract(tf.multiply(cos_t, cos_m), tf.multiply(sin_t, sin_m), name='cos_mt')

    # this condition controls the theta+m should in range [0, pi]
    #      0<=theta+m<=pi
    #     -m<=theta<=pi-m
    cond_v = cos_t - threshold
    cond = tf.cast(tf.nn.relu(cond_v, name='if_else'), dtype=tf.bool)

    keep_val = s*(cos_t - mm)
    cos_mt_temp = tf.where(cond, cos_mt, keep_val)

    mask = tf.cast(labels, tf.float32)
    inv_mask = tf.subtract(1., mask, name='inverse_mask')

    s_cos_t = tf.multiply(s, cos_t, name='scalar_cos_t')

    logit = tf.add(tf.multiply(s_cos_t, inv_mask), tf.multiply(cos_mt_temp, mask), name='arcface_loss_output')

    loss = tf.nn.softmax_cross_entropy_with_logits_v2(logits=logit, labels=labels)

    return tf.reduce_mean(loss)

## legacy code
# def ArcFaceloss(labels, features):
#     """
#     ArcFace loss function
#     """
#
#     N = tf.shape(labels)[0]
#     s = 64.
#     m1 = 1.0
#     m2 = 0.5
#     m3 = 0.
#
#     target_cos = tf.reduce_sum(tf.cast(labels, tf.float32) * features, axis=-1)
#     target_cos = tf.cos(tf.math.acos(target_cos) * m1 + m2) - m3
#     target_cos = tf.exp(s * target_cos)
#
#     others = -1. * tf.multiply(tf.subtract(tf.cast(labels, tf.float32), 1.0), features)
#     others = tf.exp(s * others)
#     others = tf.subtract(tf.reduce_sum(others, axis=-1), 1.0)
#
#     log_ = tf.log(tf.divide(target_cos, tf.add(tf.add(target_cos, others), 1e-5)))
#
#     output = -1. * tf.divide(tf.reduce_sum(log_), tf.cast(N, tf.float32))
#
#     return output


if __name__ == '__main__':
    pass
