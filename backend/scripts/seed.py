"""
초기 데이터 시드 스크립트

사용법:
    python -m scripts.seed

이 스크립트는 개발/테스트용 초기 데이터를 생성합니다.
"""
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import AsyncSessionLocal, engine
from app.models.base import Base
from app.models import Store, User, Table, Category, Menu
from app.utils.password import password_hasher


async def seed_data():
    """초기 데이터 생성"""
    
    # 테이블 생성
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    async with AsyncSessionLocal() as db:
        # 기존 데이터 확인
        from sqlalchemy import select
        result = await db.execute(select(Store).limit(1))
        if result.scalar_one_or_none():
            print("데이터가 이미 존재합니다. 시드를 건너뜁니다.")
            return
        
        # 1. 매장 생성
        store = Store(
            store_id="demo-store",
            name="데모 매장"
        )
        db.add(store)
        await db.flush()
        print(f"매장 생성: {store.name} (ID: {store.store_id})")
        
        # 2. 관리자 계정 생성
        admin = User(
            store_id=store.id,
            username="admin",
            password_hash=password_hasher.hash("admin1234")
        )
        db.add(admin)
        print(f"관리자 생성: {admin.username}")
        
        # 3. 테이블 생성 (1~5번)
        for i in range(1, 6):
            table = Table(
                store_id=store.id,
                table_number=i,
                password_hash=password_hasher.hash("1234")
            )
            db.add(table)
        print("테이블 생성: 1~5번 (비밀번호: 1234)")
        
        # 4. 카테고리 생성
        categories = [
            Category(store_id=store.id, name="메인", display_order=1),
            Category(store_id=store.id, name="사이드", display_order=2),
            Category(store_id=store.id, name="음료", display_order=3),
        ]
        for cat in categories:
            db.add(cat)
        await db.flush()
        print("카테고리 생성: 메인, 사이드, 음료")
        
        # 5. 메뉴 생성
        menus = [
            # 메인
            Menu(store_id=store.id, category_id=categories[0].id, 
                 name="김치찌개", price=8000, description="돼지고기 김치찌개", display_order=1),
            Menu(store_id=store.id, category_id=categories[0].id,
                 name="된장찌개", price=7000, description="두부 된장찌개", display_order=2),
            Menu(store_id=store.id, category_id=categories[0].id,
                 name="제육볶음", price=9000, description="매콤한 제육볶음", display_order=3),
            Menu(store_id=store.id, category_id=categories[0].id,
                 name="불고기", price=10000, description="달콤한 불고기", display_order=4),
            # 사이드
            Menu(store_id=store.id, category_id=categories[1].id,
                 name="계란말이", price=5000, description="부드러운 계란말이", display_order=1),
            Menu(store_id=store.id, category_id=categories[1].id,
                 name="김치전", price=6000, description="바삭한 김치전", display_order=2),
            # 음료
            Menu(store_id=store.id, category_id=categories[2].id,
                 name="콜라", price=2000, display_order=1),
            Menu(store_id=store.id, category_id=categories[2].id,
                 name="사이다", price=2000, display_order=2),
            Menu(store_id=store.id, category_id=categories[2].id,
                 name="소주", price=5000, display_order=3),
            Menu(store_id=store.id, category_id=categories[2].id,
                 name="맥주", price=5000, display_order=4),
        ]
        for menu in menus:
            db.add(menu)
        print(f"메뉴 생성: {len(menus)}개")
        
        await db.commit()
        print("\n✅ 시드 데이터 생성 완료!")
        print("\n접속 정보:")
        print(f"  매장 ID: demo-store")
        print(f"  관리자: admin / admin1234")
        print(f"  테이블: 1~5번 / 1234")


if __name__ == "__main__":
    asyncio.run(seed_data())
