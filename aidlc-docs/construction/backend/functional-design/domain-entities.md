# Domain Entities - Backend API

## 엔티티 관계 다이어그램

```
+----------+       +----------+       +----------------+
|  Store   |1-----*|   User   |       | TableSession   |
+----------+       +----------+       +----------------+
     |1                                      |1
     |                                       |
     *                                       *
+----------+       +----------------+  +----------+
|  Table   |1-----*| TableSession   |  |  Order   |
+----------+       +----------------+  +----------+
     |1                                      |1
     |                                       |
     *                                       *
+----------+       +----------+       +------------+
| Category |1-----*|   Menu   |       | OrderItem  |
+----------+       +----------+       +------------+
```

---

## 1. Store (매장)

### 속성
| 필드 | 타입 | 설명 | 제약조건 |
|------|------|------|----------|
| id | Integer | PK | Auto increment |
| store_id | String(50) | 매장 식별자 | Unique, Not null |
| name | String(100) | 매장명 | Not null |
| created_at | DateTime | 생성일시 | Not null, Default now |
| updated_at | DateTime | 수정일시 | Not null, Default now |

### 관계
- 1:N → User (관리자 계정)
- 1:N → Table (테이블)
- 1:N → Category (카테고리)

---

## 2. User (관리자)

### 속성
| 필드 | 타입 | 설명 | 제약조건 |
|------|------|------|----------|
| id | Integer | PK | Auto increment |
| store_id | Integer | FK → Store | Not null |
| username | String(50) | 사용자명 | Not null |
| password_hash | String(255) | 비밀번호 해시 | Not null |
| created_at | DateTime | 생성일시 | Not null |
| updated_at | DateTime | 수정일시 | Not null |

### 제약조건
- Unique: (store_id, username)

### 관계
- N:1 → Store

---

## 3. Table (테이블)

### 속성
| 필드 | 타입 | 설명 | 제약조건 |
|------|------|------|----------|
| id | Integer | PK | Auto increment |
| store_id | Integer | FK → Store | Not null |
| table_number | Integer | 테이블 번호 | Not null |
| password_hash | String(255) | 테이블 비밀번호 해시 | Not null |
| created_at | DateTime | 생성일시 | Not null |
| updated_at | DateTime | 수정일시 | Not null |

### 제약조건
- Unique: (store_id, table_number)

### 관계
- N:1 → Store
- 1:N → TableSession

---

## 4. TableSession (테이블 세션)

### 속성
| 필드 | 타입 | 설명 | 제약조건 |
|------|------|------|----------|
| id | Integer | PK | Auto increment |
| table_id | Integer | FK → Table | Not null |
| started_at | DateTime | 세션 시작 시각 | Not null |
| completed_at | DateTime | 세션 종료 시각 | Nullable |
| is_active | Boolean | 활성 여부 | Not null, Default true |

### 관계
- N:1 → Table
- 1:N → Order

---

## 5. Category (카테고리)

### 속성
| 필드 | 타입 | 설명 | 제약조건 |
|------|------|------|----------|
| id | Integer | PK | Auto increment |
| store_id | Integer | FK → Store | Not null |
| name | String(50) | 카테고리명 | Not null |
| display_order | Integer | 표시 순서 | Not null, Default 0 |
| created_at | DateTime | 생성일시 | Not null |
| updated_at | DateTime | 수정일시 | Not null |

### 제약조건
- Unique: (store_id, name)

### 관계
- N:1 → Store
- 1:N → Menu

---

## 6. Menu (메뉴)

### 속성
| 필드 | 타입 | 설명 | 제약조건 |
|------|------|------|----------|
| id | Integer | PK | Auto increment |
| store_id | Integer | FK → Store | Not null |
| category_id | Integer | FK → Category | Not null |
| name | String(100) | 메뉴명 | Not null |
| price | Integer | 가격 (원) | Not null, >= 0 |
| description | Text | 설명 | Nullable |
| display_order | Integer | 표시 순서 | Not null, Default 0 |
| is_available | Boolean | 판매 가능 여부 | Not null, Default true |
| created_at | DateTime | 생성일시 | Not null |
| updated_at | DateTime | 수정일시 | Not null |

### 관계
- N:1 → Store
- N:1 → Category

---

## 7. Order (주문)

### 속성
| 필드 | 타입 | 설명 | 제약조건 |
|------|------|------|----------|
| id | Integer | PK | Auto increment |
| session_id | Integer | FK → TableSession | Not null |
| order_number | String(20) | 주문 번호 | Not null |
| status | Enum | 주문 상태 | Not null, Default PENDING |
| total_amount | Integer | 총 금액 | Not null |
| created_at | DateTime | 주문 시각 | Not null |
| updated_at | DateTime | 수정일시 | Not null |

### OrderStatus Enum
- `PENDING` (대기중)
- `PREPARING` (준비중)
- `COMPLETED` (완료)

### 주문 번호 형식
- 형식: `YYYYMMDD-NNN`
- 예시: `20260204-001`, `20260204-002`
- 매장별, 일별 순차 번호

### 관계
- N:1 → TableSession
- 1:N → OrderItem

---

## 8. OrderItem (주문 항목)

### 속성
| 필드 | 타입 | 설명 | 제약조건 |
|------|------|------|----------|
| id | Integer | PK | Auto increment |
| order_id | Integer | FK → Order | Not null |
| menu_id | Integer | FK → Menu | Nullable (스냅샷 사용) |
| menu_name | String(100) | 메뉴명 (스냅샷) | Not null |
| unit_price | Integer | 단가 (스냅샷) | Not null |
| quantity | Integer | 수량 | Not null, >= 1 |
| subtotal | Integer | 소계 | Not null |

### 스냅샷 설계
- `menu_name`, `unit_price`: 주문 시점의 메뉴 정보 저장
- 메뉴 삭제/가격 변경 시에도 주문 내역 유지

### 관계
- N:1 → Order
- N:1 → Menu (참조용, nullable)

---

## 9. OrderHistory (주문 이력)

### 속성
| 필드 | 타입 | 설명 | 제약조건 |
|------|------|------|----------|
| id | Integer | PK | Auto increment |
| store_id | Integer | FK → Store | Not null |
| table_number | Integer | 테이블 번호 | Not null |
| session_id | Integer | 원본 세션 ID | Not null |
| order_number | String(20) | 주문 번호 | Not null |
| items_json | JSON | 주문 항목 (JSON) | Not null |
| total_amount | Integer | 총 금액 | Not null |
| ordered_at | DateTime | 주문 시각 | Not null |
| completed_at | DateTime | 이용 완료 시각 | Not null |

### items_json 구조
```json
[
  {
    "menu_name": "아메리카노",
    "unit_price": 4500,
    "quantity": 2,
    "subtotal": 9000
  }
]
```

### 관계
- N:1 → Store
