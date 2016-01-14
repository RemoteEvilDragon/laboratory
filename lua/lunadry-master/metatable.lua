Set = {}

function Set.union (a,b)
  local res = Set.new{}
  for k in pairs(a) do res[k] = true end
  for k in pairs(b) do res[k] = true end
  return res
end

function Set.intersection (a,b)
  local res = Set.new{}
  for k in pairs(a) do
    res[k] = b[k]
  end
  return res
end

function Set.tostring (set)
  local s = "{"
  local sep = ""
  for e in pairs(set) do
    s = s .. sep .. e
    sep = ", "
  end
  return s .. "}"
end

Set.mt = {}
Set.mt.__add = Set.union
Set.mt.__mul = Set.intersection

Set.mt.__le = function (a,b)    -- set containment
  for k in pairs(a) do
    if not b[k] then return false end
  end
  return true
end

Set.mt.__lt = function (a,b)
  return a <= b and not (b <= a)
end

Set.mt.__eq = function (a,b)
  return a <= b and b <= a
end

Set.mt.__tostring = Set.tostring

Set.mt.__metatable = "not your business!!"

function Set.new (t)
  local set = {}
  setmetatable(set,Set.mt)
  for _, l in ipairs(t) do set[l] = true end
  return set
end

local s1 = Set.new ({1,2,5})
local s2 = Set.new ({2,3})

print(s1+s2)
print(s1*s2)

print(s1 <= s2)       --> true
print(s1 < s2)        --> true
print(s1 >= s1)       --> true
print(s1 > s1)        --> false
print(s1 == s2 * s1)  --> true

print(getmetatable(s1))
setmetatable(s1,{})