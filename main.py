def timeDemo():
    import time
    from thaakz.utils import TimeReport

    # ── Example / smoke-test ──────────────────────────────────────────────────────
    def time_report_example1():
        tr = TimeReport("Load Tokenizer and Model")
        time.sleep(0.05)  # simulate loading

        tr.StartPhase("Tokenization")
        time.sleep(0.007)

        tr.StartPhase("Generation", startSubPhase=True)
        # next call arrives within threshold → unnamed entry is renamed
        tr.StartPhase("Resolving Config")
        time.sleep(0.033)

        tr.StartPhase("Resolving Trust_Remote_Code")
        time.sleep(0.008)

        tr.StartPhase("Internal Generation")
        time.sleep(0.12)  # shortened for demo; real run ~13s

        tr.CloseLevel()  # done with Generation sublevel

        tr.StartPhase("Displaying")
        time.sleep(0.024)

        tr.FinishedMonitoring()
        tr.PrintReport()

    def time_report_example2():
        import time
        tr = TimeReport("Leve 1")
        time.sleep(0.05)  # simulate loading

        tr.StartPhase("Leve 2", startSubPhase=True)
        time.sleep(0.07)

        tr.StartPhase("Leve 2.1")
        time.sleep(0.007)

        tr.StartPhase("Leve 2.2")
        time.sleep(0.014)
        tr.CloseLevel()  # done with Generation sublevel

        tr.StartPhase("Leve 3", startSubPhase=True)
        tr.StartPhase("Leve 3.1")
        time.sleep(0.007)

        tr.StartPhase("Leve 3.2")
        time.sleep(0.014)
        tr.CloseLevel()  # done with Generation sublevel

        tr.StartPhase("Level 4")
        time.sleep(0.033)

        tr.StartPhase("Displaying")
        time.sleep(0.024)

        tr.FinishedMonitoring()
        tr.PrintReport()

    time_report_example1()
    print("Done : time_report_example\n\n")
    time_report_example2()
    print("Done : local_example\n\n")

from pathlib import Path
from typing import Literal

def TypeTreeDemo(jsonfile: Path | str):
    jsonfile = Path(jsonfile)

    # Create the directory if it doesn't exist
    jsonfile.mkdir(parents=True, exist_ok=True)

    # Ensure it's a directory
    if not jsonfile.is_dir():
        raise NotADirectoryError(f"{jsonfile} is not a directory.")

    from thaakz.utils import CentralRegistry, TypeTree
    # from type_tree import describe_class

    tree_path = jsonfile / "demo_tree.tjson"
    catalog_path = jsonfile / "demo_catalog.tjson"
    demo_registry = CentralRegistry()
    tree = TypeTree(path=tree_path, registry=demo_registry)

    # ---------------------------------------------------------------------
    # 1) A simple local hierarchy -- BEFORE registering it, so you can see
    #    the honest "unregistered:" fallback in action.
    # ---------------------------------------------------------------------
    class Animal:
        pass

    class Mammal(Animal):
        pass

    class Bird(Animal):
        pass

    class Dog(Mammal):
        pass

    class Cat(Mammal):
        pass

    tree.append(Dog)
    tree.append(Cat)
    tree.append(Bird)

    print("=== After appending Dog, Cat, Bird (local package NOT yet registered) ===")
    print(demo_registry.resolve_package(Animal.__module__))
    print()

    # ---------------------------------------------------------------------
    # 2) Builtins share 'object' as the same root -- merge across totally
    #    different appended types.
    # ---------------------------------------------------------------------
    tree.append(bool)
    tree.append(int)

    # ---------------------------------------------------------------------
    # 3) Save the merged tree + the registry's flat catalog.
    # ---------------------------------------------------------------------

    tree.save()
    demo_registry.save_catalog(catalog_path)

    print("=== Roots in the tree ===")
    for r in tree._roots:
        print(r, "->", tree.get(r)["qualified_name"])

    print()
    print("=== describe_class() on Dog (same style as your original function, enriched) ===")
    demo_registry.describe(Dog)

    # ---------------------------------------------------------------------
    # 4) Honesty check: diamond / multiple inheritance caveat.
    #    Because __mro__ linearizes multiple inheritance PER CLASS, the same
    #    ancestor can end up with a different "immediate parent" depending on
    #    which subclass you started from. TypeTree will still recognize it as
    #    the SAME node (same id everywhere) but it may appear under more than
    #    one parent in the nested tree view.
    # ---------------------------------------------------------------------
    class Swimmer:
        pass

    class Runner:
        pass

    class Amphibious(Swimmer, Runner):
        pass  # diamond-ish: two direct parents

    tree2 = TypeTree(registry=demo_registry)
    tree2.append(Amphibious)
    print()
    print("=== Amphibious MRO (diamond example) ===")

    for c in Amphibious.__mro__:
        print(" ", c.__module__ + "." + c.__qualname__)

def MP4ToImages(video_path: Path | str,
                start: float | int = 0,
                end: float | int = -1,
                gap: float | int = -1,
                unit: Literal["frames", "time", "percent"] = "frames"):

    video_path = Path(video_path)
    if not video_path.is_file():
        print(f"Path: {video_path}, is not a valid path!")
        return

    if unit not in ("frames", "time", "percent"):
        print(f"Unit: {unit} is not valid! Must be 'frames', 'time', or 'percent'.")
        return

    if start < 0:
        print(f"Frame start: {start} is not valid!")
        return

    if end != -1 and end < start:
        print(f"Frame end: {end} is not valid!")
        return

    if gap != -1 and gap <= 0:
        print(f"Frame gap: {gap} is not valid!")
        return

    if unit == "percent" and (start > 100 or (end != -1 and end > 100) or (gap != -1 and gap > 100)):
        print("Percent values must be within [0, 100]!")
        return

    import cv2
    output_dir = video_path.parent / video_path.stem
    output_dir.mkdir(parents=True, exist_ok=True)

    cap = None
    try:
        cap = cv2.VideoCapture(str(video_path))
        if not cap.isOpened():
            print(f"CV2 could not open video file: {video_path}!")
            return

        frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        print(f"Total frames: {int(frame_count)}")

        fps = cap.get(cv2.CAP_PROP_FPS)
        if fps <= 0:
            print("Unable to get fps information!")
        else:
            print(f"FPS = {fps}!")

        # Resolve conversion factor: raw unit value -> frames
        if unit == "time":
            if fps <= 0:
                print("Unable to get fps information! So interval in time unit is not defined!")
                return
            frame_per_unit = fps
        elif unit == "percent":
            if frame_count <= 0:
                print("Unable to get total frame count! So interval in percent unit is not defined!")
                return
            frame_per_unit = frame_count / 100.0
        else:  # frames
            frame_per_unit = 1.0

        start *= frame_per_unit
        end = frame_count if end == -1 else end * frame_per_unit
        if end > frame_count:
            end = frame_count

        if start > end:
            print("Empty range detected!")
            return

        gap = (0.5 * fps if fps > 0 else 15.0) if gap == -1 else gap * frame_per_unit

        float_pos: float = start
        frame_idx = 0
        saved = 0

        while True:
            ret, frame = cap.read()
            if not ret:
                break
            if frame_idx >= float_pos:
                filename = output_dir / f"frame_{saved:05d}.png"
                cv2.imwrite(str(filename), frame)
                saved += 1
                float_pos += gap
                if float_pos > end:
                    break
            frame_idx += 1

        print(f"Saved {saved} frames to '{output_dir}'")

    except Exception as e:
        print(f"Failed to open video {video_path} due to error: {e}")
        return
    finally:
        if cap is not None:
            cap.release()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    timeDemo()
    TypeTreeDemo("output/json")
    MP4ToImages(video_path="203874-922675723.mp4", gap=1)
