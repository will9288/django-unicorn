import test from "ava";
import { getElement } from "../utils.js";

test("poll", (t) => {
  const html = "<div unicorn:poll='test()'></div>";
  const element = getElement(html);

  t.is(element.poll.method, "test()");
  t.is(element.poll.timing, 2000);
});

test("poll.1000", (t) => {
  const html = "<div unicorn:poll.1000='test()'></div>";
  const element = getElement(html);

  t.is(element.poll.timing, 1000);
});
