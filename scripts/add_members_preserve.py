
"""
Bo sung thanh vien 043 vao 20 anh.
Giu nguyen phan cong cua 044, 065, 067.
Khong thay doi cac file COCO da export.

Chay:
    python scripts/add_members_preserve.py
"""

import csv
import shutil
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parent.parent

QC_DIR = ROOT / "submission" / "qc"
ASSIGNMENT = QC_DIR / "assignment.csv"
BACKUP = QC_DIR / "assignment_backup.csv"
ASSIGNMENTS_DIR = QC_DIR / "assignments"

IMAGES_DIR = ROOT / "data" / "images"
WORK_DIR = ROOT / "work"

OLD_MEMBERS = {"044", "065", "067"}
NEW_MEMBER = "043"
NUM_NEW_IMAGES = 20

FIELDS = ["image", "annotators", "n_annotators"]


def read_assignment(path):
    with path.open(
        "r", encoding="utf-8-sig", newline=""
    ) as f:
        reader = csv.DictReader(f)

        if reader.fieldnames != FIELDS:
            raise SystemExit(
                f"Sai cot trong {path.name}"
            )

        return list(reader)


def main():
    if not BACKUP.is_file():
        raise SystemExit(
            "Khong tim thay assignment_backup.csv"
        )

    if not ASSIGNMENT.is_file():
        raise SystemExit(
            "Khong tim thay assignment.csv"
        )

    original = read_assignment(BACKUP)
    current = read_assignment(ASSIGNMENT)

    # Khong ghi de neu assignment da thay doi
    if current != original:
        raise SystemExit(
            "assignment.csv khac ban backup. "
            "Dung lai de tranh ghi de phan cong."
        )

    if len(original) != 40:
        raise SystemExit(
            "Bang phan cong phai co 40 anh."
        )

    image_names = [r["image"] for r in original]

    if len(set(image_names)) != 40:
        raise SystemExit("Co ten anh bi trung.")

    # Kiem tra phan cong cu va file anh
    for row in original:
        members = row["annotators"].split("|")

        if (
            len(members) != 2
            or len(set(members)) != 2
            or not set(members) <= OLD_MEMBERS
            or row["n_annotators"] != "2"
        ):
            raise SystemExit(
                f"Phan cong cu khong hop le: {row}"
            )

        if not (IMAGES_DIR / row["image"]).is_file():
            raise SystemExit(
                f"Thieu anh: {row['image']}"
            )

    # Chon 20 anh xen ke theo ten anh
    selected = set(sorted(image_names)[::2])

    if len(selected) != NUM_NEW_IMAGES:
        raise SystemExit("Khong chon du 20 anh.")

    updated_rows = []
    member_images = {
        m: [] for m in sorted(
            OLD_MEMBERS | {NEW_MEMBER}
        )
    }

    for row in original:
        image_name = row["image"]
        old_members = row["annotators"].split("|")

        if image_name in selected:
            members = sorted(
                old_members + [NEW_MEMBER]
            )
        else:
            members = old_members.copy()

        updated_rows.append({
            "image": image_name,
            "annotators": "|".join(members),
            "n_annotators": len(members)
        })

        for member in members:
            member_images[member].append(image_name)

    # Tien hanh backup rieng truoc khi ghi
    safety_backup = QC_DIR / "assignment_before_043.csv"

    shutil.copy2(ASSIGNMENT, safety_backup)

    # Tao thu muc anh cho 043
    target = WORK_DIR / NEW_MEMBER / "images"
    target.mkdir(parents=True, exist_ok=True)

    # Khong xoa anh co san trong work/043
    existing = list(target.iterdir())

    if existing:
        raise SystemExit(
            "work/043/images/ da co du lieu. "
            "Hay kiem tra truoc khi chay."
        )

    # Copy 20 anh cho 043
    for image_name in member_images[NEW_MEMBER]:
        shutil.copy2(
            IMAGES_DIR / image_name,
            target / image_name
        )

    # Tao danh sach rieng tung thanh vien
    ASSIGNMENTS_DIR.mkdir(
        parents=True, exist_ok=True
    )

    for member, images in member_images.items():
        file_path = (
            ASSIGNMENTS_DIR / f"{member}.txt"
        )

        if file_path.exists():
            raise SystemExit(
                f"File {file_path.name} da ton tai."
            )

        file_path.write_text(
            "\n".join(images) + "\n",
            encoding="utf-8"
        )

    # Cap nhat assignment.csv
    with ASSIGNMENT.open(
        "w", encoding="utf-8", newline=""
    ) as f:
        writer = csv.DictWriter(
            f, fieldnames=FIELDS
        )
        writer.writeheader()
        writer.writerows(updated_rows)

    # Hien thi ket qua
    print("\n===== CAP NHAT THANH CONG =====")
    print("Tong so anh:", len(updated_rows))
    print("Thanh vien moi:", NEW_MEMBER)

    counts = Counter()

    for row in updated_rows:
        for member in row["annotators"].split("|"):
            counts[member] += 1

    for member in sorted(counts):
        print(
            f"Thanh vien {member}: "
            f"{counts[member]} anh"
        )

    print("\n043 duoc them vao 20 anh.")
    print("Phan cong cua 3 nguoi cu duoc giu nguyen.")
    print("Khong thay doi file COCO.")
    print("Da cap nhat assignment.csv.")
    print("Da tao file assignments/043.txt.")
    print("Da copy anh vao work/043/images/.")


if __name__ == "__main__":
    main()
