"""Run isolated requests; persist all question step logs in one text file."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import time
from datetime import datetime

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent


def worker(index):
    sys.path.insert(0, str(PROJECT.parent))
    from backend.app.main import ask
    from backend.app.models import AskRequest
    case = json.loads((HERE / 'questions_50.json').read_text(encoding='utf-8'))[index]
    response = ask(AskRequest(question=case['question']))
    print('BENCHMARK_RESPONSE=' + response.model_dump_json(), flush=True)


def run():
    cases = json.loads((HERE / 'questions_50.json').read_text(encoding='utf-8'))
    assert len(cases) == 50
    folder = HERE / ('run_' + datetime.now().strftime('%Y%m%d_%H%M%S'))
    folder.mkdir()
    combined = folder / 'all_questions.txt'
    results = []
    start = time.perf_counter()
    print(f'OUTPUT_FOLDER={folder}', flush=True)
    with combined.open('w', encoding='utf-8', buffering=1) as all_log:
        all_log.write(f'50-question benchmark\nProject: {PROJECT}\n'
                      'Each question is independent; invokes the same /ask handler directly to capture terminal steps.\n'
                      'PASS means expected status matched; SQL/result correctness requires manual review.\n'
                      'Timeout: 180 seconds per question. This combined log is updated and flushed after each question.\n\n')
        for index, case in enumerate(cases):
            started = time.perf_counter()
            header = f"Question {index+1}/50: {case['question']}\nExpected status: {case['expected_status']}\n"
            env = dict(os.environ, PYTHONUNBUFFERED='1', PYTHONIOENCODING='utf-8', PYTHONDONTWRITEBYTECODE='1')
            proc = subprocess.Popen([sys.executable, '-B', str(Path(__file__).resolve()), '--worker', str(index)],
                                    cwd=PROJECT, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
                                    encoding='utf-8', errors='replace', env=env)
            timed_out = False
            try:
                output, _ = proc.communicate(timeout=180)
            except subprocess.TimeoutExpired:
                timed_out = True
                proc.kill()
                output, _ = proc.communicate()
                output += '\nBENCHMARK TIMEOUT: worker stopped after 180 seconds.\n'
            duration = time.perf_counter() - started
            content = header + output
            response = None
            for line in content.splitlines():
                if line.startswith('BENCHMARK_RESPONSE='):
                    response = json.loads(line.removeprefix('BENCHMARK_RESPONSE='))
            status = response['status'] if response else ('timeout' if timed_out else 'worker_error')
            passed = status == case['expected_status']
            result = dict(number=index+1, question=case['question'], expected_status=case['expected_status'],
                          actual_status=status, passed=passed, wall_seconds=round(duration, 3))
            results.append(result)
            footer = f'\nBENCHMARK RESULT: {"PASS" if passed else "FAIL"} | Actual: {status} | Wall time including worker startup: {duration:.3f}s\n'
            all_log.write(content + footer + '\n' + '='*80 + '\n')
            all_log.flush()
            os.fsync(all_log.fileno())
            (folder / 'results.json').write_text(json.dumps(results, indent=2), encoding='utf-8')
            print(f'{index+1:02}/50 {"PASS" if passed else "FAIL"} {status} {duration:.1f}s | saved all_questions.txt', flush=True)
        summary = f'Completed 50 questions. Status matches: {sum(r["passed"] for r in results)}/50. Total benchmark time: {time.perf_counter()-start:.1f}s.'
        all_log.write(summary + '\n')
        all_log.flush()
        os.fsync(all_log.fileno())
        print(summary, flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--worker', type=int)
    args = parser.parse_args()
    if args.worker is not None:
        worker(args.worker)
    else:
        run()
