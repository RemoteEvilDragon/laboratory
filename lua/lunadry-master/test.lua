local function len(list)
local count = 0
                for k,v in pairs(list) do
                    count = count + 1
                end
return count
end
local function _t(k,v)
assert(type(k) == "string","Parameter k must be a string type!!")

return {[k]=v}
end

local jsonString = 
                {
                _t("shaderName","customTest"),
                _t("vert","res/shaders/test_vert.c"),
                _t("frag","res/shaders/test_frag.c"),
                _t("iResolution" , {1080,768,0} )
                }

local t = {
1,

"ab",

_t("name",{"athen",1,2,_t("b",{1,2}) } ),
_t("abc",3),_t("aaa",{2,"a",_t("b",{"c",1,1})} ),false,4}
local function easytable2json(list)
local function innerFunc(t)
local tm = {}
for k,v in pairs(t) do
if type(v) ~= "table" then--value k
    if type(v) == "number" or type(v) == "boolean" then
    table.insert(tm,tostring(v))
    else
    table.insert(tm,"\""..tostring(v).."\"")
    end
else--real k
    --unevelop brackets here
assert(len(v) == 1,"invalid data format!!!")

for kk,vv in pairs(v) do
local str = ""
str = str.."\""..kk.."\""..":"
if type(vv) == "table" then
    str = str..innerFunc(vv)
else
if type(vv) == "number" then
    str = str..tostring(vv)
else
    str = str.."\""..tostring(vv).."\""
end
end
table.insert(tm,str)
break
end
end
end
return "["..table.concat(tm,",").."]"
end

local str = string.sub(innerFunc(list),2)
str = string.sub(str,1,-2)
return "{"..str.."}"
end
print("json is "..easytable2json(t))