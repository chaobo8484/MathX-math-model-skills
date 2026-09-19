#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
main.py —— @PROBLEM@ 总入口（论文附录提交版）

定位：不直接运行。它是整题代码的浓缩索引，供论文附录提交、
审稿人循迹。单问复现去各问脚本目录执行对应脚本。

问数：@N@（q1..q@N@），顺序执行。
目录约定：
  qN/data_qN/       该问原始数据（raw）
  qN/cleaned_data/  该问清洗后数据（processed，ingest-inputs 输出）
  qN/script_qN/     该问脚本（本文件只索引，不贴全文）
  qN/charts_qN/     该问图表输出
环境：python >= 3.10；第三方依赖见各问脚本头注释。
"""

@BLOCKS@

def main():
    """按问顺序执行（每行调一问，函数名填实后取消注释）。"""
@CALLS@
    print("全部问题执行完毕，图表见各问 charts_qN/，清洗数据见 cleaned_data/")


if __name__ == "__main__":
    main()
