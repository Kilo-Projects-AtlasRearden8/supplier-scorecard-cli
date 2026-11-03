"""Command-line interface for the Supplier Scorecard."""

import argparse
import sys
import uuid
from datetime import date

from .models import Supplier, LeadTimeRecord, validate_quality
from .scoring import score_suppliers
from .storage import Storage
from .export import export_csv


def new_id():
    return uuid.uuid4().hex[:8]


def cmd_add(args, storage):
    suppliers = storage.load()
    if any(s.name.lower() == args.name.lower() for s in suppliers):
        print(f"A supplier named '{args.name}' already exists.")
        return 1
    try:
        quality = validate_quality(args.quality)
    except ValueError as e:
        print(f"Error: {e}")
        return 1
    supplier = Supplier(
        id=new_id(),
        name=args.name,
        price=float(args.price),
        quoted_lead_time=int(args.lead_time),
        quality=quality,
        notes=args.notes or "",
    )
    suppliers.append(supplier)
    storage.save(suppliers)
    print(f"Added supplier {supplier.id}: {supplier.name}")
    return 0


def cmd_list(args, storage):
    suppliers = storage.load()
    scored = score_suppliers(suppliers)
    if not scored:
        print("No suppliers found. Add one with: supplier-scorecard add --name ...")
        return 0
    print(f"{'Rank':<5} {'ID':<10} {'Name':<26} {'Price':<8} {'LeadTime':<9} {'Quality':<9} {'Score':<7}")
    for r in scored:
        s = r.supplier
        print(
            f"{r.rank:<5} {s.id:<10} {s.name:<26} {s.price:<8.2f} "
            f"{s.quoted_lead_time:<9} {s.quality:<9.1f} {r.overall_score:<7.2f}"
        )
    return 0


def cmd_record(args, storage):
    suppliers = storage.load()
    found = None
    for s in suppliers:
        if s.id == args.id:
            found = s
            break
    if not found:
        print(f"Supplier {args.id} not found.")
        return 1
    quoted = args.quoted if args.quoted is not None else found.quoted_lead_time
    record = LeadTimeRecord(
        date=str(date.today()),
        quoted_days=int(quoted),
        actual_days=int(args.actual),
        reference=args.reference or "",
    )
    found.lead_times.append(record)
    storage.save(suppliers)
    print(
        f"Recorded lead time for {found.name}: actual={args.actual} days "
        f"(quoted {quoted}) on {record.date}"
    )
    return 0


def cmd_show(args, storage):
    """Show detailed supplier info including lead time history."""
    suppliers = storage.load()
    found = None
    for s in suppliers:
        if s.id == args.id:
            found = s
            break
    if not found:
        print(f"Supplier {args.id} not found.")
        return 1
    scored = score_suppliers([found] + [s for s in suppliers if s.id != found.id])
    r = scored[0]
    s = found
    print(f"Supplier: {s.name} (ID: {s.id})")
    print(f"  Price: ${s.price:.2f}")
    print(f"  Quoted Lead Time: {s.quoted_lead_time} days")
    print(f"  Quality: {s.quality}/5")
    print(f"  Notes: {s.notes or '(none)'}")
    print(f"  Scores: Price={r.price_score:.1f}, Speed={r.speed_score:.1f}, Quality={r.quality_score:.1f}, Overall={r.overall_score:.1f} (Rank #{r.rank})")
    if s.lead_times:
        print("  Lead Time History:")
        for lt in s.lead_times:
            diff = lt.actual_days - lt.quoted_days
            status = "early" if diff < 0 else ("late" if diff > 0 else "on time")
            print(f"    {lt.date}: quoted {lt.quoted_days}d, actual {lt.actual_days}d ({status}){f', ref: {lt.reference}' if lt.reference else ''}")
    else:
        print("  Lead Time History: (none recorded)")
    return 0


def cmd_remove(args, storage):
    suppliers = storage.load()
    initial_len = len(suppliers)
    suppliers = [s for s in suppliers if s.id != args.id]
    if len(suppliers) == initial_len:
        print(f"Supplier {args.id} not found.")
        return 1
    storage.save(suppliers)
    print(f"Removed supplier {args.id}.")
    return 0


def cmd_export(args, storage):
    suppliers = storage.load()
    scored = export_csv(suppliers, path=args.output)
    print(f"Exported {len(scored)} suppliers to {args.output}")
    return 0


def build_parser():
    parser = argparse.ArgumentParser(
        prog="supplier-scorecard",
        description="Score resale suppliers on price, speed, and quality (local-first, no keys).",
    )
    parser.add_argument("--storage", default="suppliers.json", help="Path to local JSON storage file")
    sub = parser.add_subparsers(dest="command", required=True)

    p_add = sub.add_parser("add", help="Add a supplier")
    p_add.add_argument("--name", required=True, help="Supplier name")
    p_add.add_argument("--price", required=True, type=float, help="Unit cost")
    p_add.add_argument(
        "--lead-time", required=True, type=int, dest="lead_time", help="Quoted lead time in days"
    )
    p_add.add_argument("--quality", required=True, type=float, help="Quality rating 1-5")
    p_add.add_argument("--notes", default="", help="Notes")
    p_add.set_defaults(func=cmd_add)

    p_list = sub.add_parser("list", help="List and score suppliers")
    p_list.set_defaults(func=cmd_list)

    p_record = sub.add_parser("record", help="Record an actual lead time")
    p_record.add_argument("--id", required=True, help="Supplier id")
    p_record.add_argument("--actual", required=True, type=int, dest="actual", help="Actual lead time in days")
    p_record.add_argument("--quoted", type=int, dest="quoted", help="Quoted lead time (defaults to supplier's)")
    p_record.add_argument("--reference", default="", help="PO/reference number")
    p_record.set_defaults(func=cmd_record)

    p_show = sub.add_parser("show", help="Show supplier details and lead time history")
    p_show.add_argument("--id", required=True, help="Supplier id")
    p_show.set_defaults(func=cmd_show)

    p_remove = sub.add_parser("remove", help="Remove a supplier")
    p_remove.add_argument("--id", required=True, help="Supplier id")
    p_remove.set_defaults(func=cmd_remove)

    p_export = sub.add_parser("export", help="Export suppliers to CSV")
    p_export.add_argument("--output", default="suppliers.csv", help="Output CSV path")
    p_export.set_defaults(func=cmd_export)

    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    storage = Storage(args.storage)
    return args.func(args, storage) or 0


if __name__ == "__main__":
    sys.exit(main())
