#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
import sys

from jarvis_ipybox.executor import ExecutionClient


async def main():
    # 연결 정보 설정
    host = "localhost"
    port = 8080  # 기본 Jupyter Kernel Gateway 포트

    try:
        # ExecutionClient 인스턴스 생성 및 연결
        print("커널에 연결합니다...")
        async with ExecutionClient(host=host, port=port) as client:
            print(f"커널 연결 완료. 커널 ID: {client.kernel_id}")

            # CSV 파일 생성 코드
            csv_code = """
import pandas as pd
import numpy as np
import os

# 샘플 데이터 생성
data = {
    '이름': ['김철수', '이영희', '박민수', '정지원', '최수진'],
    '나이': [28, 34, 42, 25, 31],
    '직업': ['개발자', '디자이너', '마케터', '연구원', '교사'],
    '급여': [3500000, 3200000, 4100000, 3800000, 2900000],
    '입사일': ['2020-03-15', '2018-09-20', '2015-12-01', '2021-06-10', '2019-04-05']
}

# DataFrame 생성
df = pd.DataFrame(data)

# 현재 작업 디렉토리 확인
current_dir = os.getcwd()
print(f"현재 작업 디렉토리: {current_dir}")

# CSV 파일로 저장
output_path = os.path.join(current_dir, 'employee_data.csv')
df.to_csv(output_path, index=False, encoding='utf-8')
print(f"CSV 파일이 다음 위치에 저장되었습니다: {output_path}")

# 저장된 파일 내용 확인
print("저장된 CSV 파일 내용 미리보기:")
print(df.head())
"""

            # 코드 실행
            print("코드를 실행합니다...")
            result = await client.execute(csv_code)

            # 실행 결과 출력
            print("\n실행 결과:")
            if result.text:
                print(result.text)

            # 이미지 결과가 있는 경우 처리
            if result.images:
                print(f"\n생성된 이미지 수: {len(result.images)}")
                for i, img in enumerate(result.images):
                    print(f"이미지 {i+1} 크기: {img.size}")

            print("\n커널 연결을 종료합니다...")

        print("커널이 성공적으로 종료되었습니다.")

    except Exception as e:
        print(f"오류 발생: {str(e)}")
        if hasattr(e, "trace") and e.trace:
            print(f"오류 추적: {e.trace}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
