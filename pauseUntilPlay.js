function pauseUntilPlay(poll=0.5) {
  // Pauses time until "play" (Set normal time rate) button is pressed 
  // Note: keyboard shortcut ('K' by default) does not work while the script is running
  var rate = core.getTimeRate();  // save current time rate
  core.setTimeRate(0.0);  // pause the script
  var now = core.getMJDay();
  do {
    core.wait(poll);  // wait to avoid freeze
  } while (core.getMJDay() == now);  // wait for "play" button
  core.setTimeRate(rate);  // restore original time rate
}