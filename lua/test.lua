function orderedTable2json(t)
    local function serialize(tbl)
        local tmp = {}
        local count = 0
        for _,t in ipairs(tbl) do
            for k, v in pairs(t) do
                local k_type = type(k)
                local v_type = type(v)


                local key = (k_type == "string" and "\"" .. k .. "\":")
                    or (k_type == "number" and "")

                local value = (v_type == "table" and serialize(v))
                    or (v_type == "boolean" and tostring(v))
                    or (v_type == "string" and "\"" .. v .. "\"")
                    or (v_type == "number" and v)

                tmp[#tmp + 1] = key and value and tostring(key) .. tostring(value) or nil
            end
            count = count + 1
        end

        if count == 0 then
            return "{" .. table.concat(tmp, ",") .. "}"
        else
            return "[" .. table.concat(tmp, ",") .. "]"
        end
    end
    assert(type(t) == "table")
    return serialize(t)
end

--this is a bad method,not good for iterating.
local k_m = {
{le = { {level=1},{b=3} }  },
-- {le = 1  },
{cu2=2},
{combo=3},
{perfect=4}
}

-- local k_m = {a_le=1,b_lee=1,c_cu2=2,d_combo=3,e_perfect=4}
print(orderedTable2json(k_m))

-- for _,t in ipairs(k_m) do
--     for k,v in pairs(t) do
--     	print(k)
--     	print("\n")
--     	print(v)
--     end
-- end
