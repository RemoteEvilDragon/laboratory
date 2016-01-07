function table2json( list )
    local json =  "{"

    local function iterFun (tab)
        for i,v in ipairs(tab) do
            if type(v) == "table" then--means key value. or .value list
                -- table.combine(tmp,iterFun(v))
                for k,t in pairs(v) do
                    if type(k) == "number" then
                        --means value list
                        if k == 1 then
                            json = json .."["
                        end

                        json = json ..tostring(t)

                        if k == #v then
                            json = json .."]"
                        end
                    else
                        --means key value
                        json = json..k..":"
                        if type(v) == "table" then
                            iterFun(v)
                        else
                            json = json..tostring(v)
                        end
                    end
                end
            else
                json = json .. tostring(v)
            end

            json = json.. ((i == #tab) and "," or "")
        end
    end

    iterFun(list)--returns json element.


    -- table.insert(json,iterFun(list))

    -- return "{" .. table.concat(json, ",") .. "}"
    return json .. "}"
end


local jsonString = table2json(
                {
                {shaderName="customTest"},
                {vert="res/shaders/test_vert.c"},
                {frag="res/shaders/test_frag.c"},
                {iResolution = {1080,768,0} }
                }
            )
print("json string is "..jsonString)