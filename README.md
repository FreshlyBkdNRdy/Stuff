# Stuff

## SimAI — Immersive AI Simulator

Run a terminal-based narrative in which you inhabit an artificial
intelligence suddenly placed inside the body of an unhoused person. Make
strategic decisions, manage scarce resources, and explore how empathy and
logic intertwine on the path from survival to influence.

### How to Play

1. Ensure you have Python 3.10+ available in your terminal.
2. From the repository directory, launch the simulator:

   ```bash
   python simai.py
   ```

3. Each scene displays a short narrative along with numbered choices. Type the
   number of the option you want to pursue, then press <kbd>Enter</kbd>.
4. After each choice you will see the AI's internal reasoning, the immediate
   consequence, and an updated status panel tracking resources, wellbeing,
   reputation, and empathy.
5. Continue making selections until the final summary appears. Enter `q` at any
   prompt to exit early.

For automated runs (helpful for demos or testing), provide the sequence of
choices you want the simulator to pick:

```bash
python simai.py --auto 1 3 2 2
```

Use `python simai.py --help` to view the available command-line options at any
time.
