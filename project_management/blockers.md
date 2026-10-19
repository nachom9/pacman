# Blocking points and issues

Dates come from the git history. Cause and fix are described as they
happened and can be checked in the commits.

## 1. Ghosts out of control after being eaten (7-9 Oct)

- **Symptom:** after Pac-Man ate a ghost it left the map, crossed inner walls
  or went left and right forever.
- **Cause:** eaten ghosts move at speed 4. A cell is 54 px and 54 is not a
  multiple of 4, so with a fixed step the ghost jumped over the centre of
  every second cell. Ghosts only turn at centres, so when a turn was needed
  they could not align and went straight, and the move code did not check
  walls in that case. The cell was also read with `//`, which changes cell
  halfway between centres, so the BFS started from a wrong cell.
- **Earlier approach:** force the parity of the coordinate depending on the
  speed (`fix_coords`, added on 7 Oct as `new coords fix method`, with a
  special case for speed 4) and an extra "re-centre" state (`center_ghost`
  and the `fixed` flag). It worked for some speeds only and the extra state
  was hard to follow.
- **Solution (9 Oct, `new movement structure`):** a ghost picks a direction
  only at a cell centre; every step is limited to the distance to the next
  centre, so it can never jump over one; the cell is the nearest one, not
  `//`. This made `fix_coords`, `center_ghost`, `predict_move` and the ghosts'
  wall check unnecessary.
- **Check:** 600,000 simulated frames with speed changes in the middle of
  corridors (`test_plan.md`, G2).
- **Lesson:** fix the cause (never skip a centre) and not the symptom for
  each speed.

## 2. `IndexError` in non-square mazes (15 Oct)

- **Symptom:** crash in the ghosts' target calculation when the maze was not
  square (commit `multi-size levels fixes`).
- **Cause:** rows and columns were mixed up (`len(maze[0])` used for rows in
  the targets). It did not show while every maze was 15x15.
- **Solution:** rows use `len(maze)` and columns `len(maze[0])`; the target is
  kept inside the maze. Levels of different sizes were added to the default
  config so this is seen every time the game runs.
- **Check:** targets tested for the four ghosts on 256 maze sizes (G1).

## 3. Pac-Man spawning inside the "42" (15 Oct)

- **Cause:** the generator draws a "42" of closed cells in the centre of big
  mazes, and Pac-Man started in the exact centre.
- **Solution:** Pac-Man starts on the free cell closest to the centre
  (`find_spawn_cell`), and pacgums are not placed in closed cells.

## 4. Several super-pacgums close together (9 Oct)

- **Symptom:** if Pac-Man ate a super-pacgum before the effect of the
  previous one had ended, strange things happened, for example the ghosts
  stayed in flee mode forever. Commit `multiple big pacgum in time bug fix`.
- **Cause:** the flee timer was not reset correctly when a new super-pacgum
  was eaten, and the counter tracking the end of the effect was not handled
  correctly. When a ghost was eaten, it incremented the counter so Pac-Man
  could return to normal mode once all four ghosts had finished fleeing or
  had been eaten. However, if Pac-Man ate a ghost and then another super-pacgum,
  the counter was not properly reset, so the new effect ended after only three
  ghosts instead of four.
- **Solution:** added and modified lines of code to correctly reset the flee
  timers and manage the counter when a new super-pacgum is eaten. This ensures
  that the four ghosts are accounted for correctly, whether they are eaten or
  finish fleeing naturally, and that Pac-Man and the ghosts return to their
  normal states at the right time.
- **How to test it:** eat a second super-pacgum while the ghosts are still
  blue and check that they go back to chasing at the end (`test_plan.md`,
  G5b).

## 5. Going back to the main menu (13 Oct)

- **Problem:** the first solution called `main()` again.
- **Cause:** it worked, but each game added a call to the stack and repeated
  the whole start-up (config, `pygame.init`, assets and warnings).
- **Solution:** one start-up and a `while` loop around the menu and the
  levels.

## 6. Blinking text on the game over screen (10 Oct)

- **Problem:** the text stayed visible after being drawn once.
- **Cause:** pygame does not clear the screen; what is drawn stays until
  something is drawn over it.
- **Solution:** every frame the whole screen is cleared and redrawn; the
  blinking text is drawn only on some frames.

## 7. Highscore file on the first run (13 Oct)

- **Problem:** the first save failed because the file did not exist.
- **Cause:** `save_score` read the file before writing, and reading a missing
  file raised `FileNotFoundError`.
- **Solution:** `load_scores` catches read errors and returns an empty list,
  so the first save creates the file.
