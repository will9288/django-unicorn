import test from "ava";
import { getElement } from "../utils.js";

test("isUnicorn", (t) => {
  const html = "<input unicorn:model='name'></input>";
  const element = getElement(html);

  t.true(element.isUnicorn);
});

test("!isUnicorn", (t) => {
  const html = "<input></input>";
  const element = getElement(html);

  t.false(element.isUnicorn);
});

test("key", (t) => {
  const html = "<input unicorn:model='name' unicorn:key='testKey'></input>";
  const element = getElement(html);

  t.is(element.key, "testKey");
});

test("unicorn:id is not an action", (t) => {
  const html = "<div unicorn:id='asdf'></div>";
  const element = getElement(html);

  t.true(element.isUnicorn);
  t.deepEqual(element.action, {});
});

test("unicorn:key is not an action", (t) => {
  const html = "<div unicorn:key='hjkl'></div>";
  const element = getElement(html);

  t.true(element.isUnicorn);
  t.deepEqual(element.action, {});
});

test("unicorn:checksum is not an action", (t) => {
  const html = "<div unicorn:checksum='fghj'></div>";
  const element = getElement(html);

  t.true(element.isUnicorn);
  t.deepEqual(element.action, {});
});
