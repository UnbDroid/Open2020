-- Inicio das funçoes de base para operaçoes bitwise
function lshift(x, by)
  return x * 2 ^ by
end

function BitOR(a,b)--Bitwise or
    local p,c=1,0
    while a+b>0 do
        local ra,rb=a%2,b%2
        if ra+rb>0 then c=c+p end
        a,b,p=(a-ra)/2,(b-rb)/2,p*2
    end
    return c
end

function bitAND(a, b)
    local result = 0
    local bitval = 1
    while a > 0 and b > 0 do
      if a % 2 == 1 and b % 2 == 1 then -- test the rightmost bits
          result = result + bitval      -- set the current bit
      end
      bitval = bitval * 2 -- shift left
      a = math.floor(a/2) -- shift right
      b = math.floor(b/2)
    end
    return result
end

-- Fim das funçoes de base para operaçoes bitwise

-- Variaveis Globais para calculo do TSP

n=4; -- Numero de blocos + 1
INT_MAX = 999999
dist = {}          -- Criando a matriz
for i=1,n do
    dist[i] = {}     -- Criando linhas da matriz
    for j=1,n do
        dist[i][j] = 0
    end
end
dist = {        -- Alocando parametros da matriz
    {0, 10, 20, 3},
    {10, 0, 2, 10},
    {2, 20, 0, 30},
    {30, 2, 30, 0}
}

VISITED_ALL = lshift(1,n+1) - 1;

cityOrder = {0,0,0,0}

-- dp[16][4];
dp = {}          -- Criando a matriz da programaçao dinamica
for i=1,VISITED_ALL do
    dp[i] = {}     -- Criando linhas da matriz
    for j=1,n do
        dp[i][j] = -1
    end
end

-- Fim das variaveis globais do TSP


function sysCall_init()
    -- do some initialization here
end




function  tsp(mask, pos) -- Funçao para calcular o melhor caminho: tsp(1,1)
	if(mask==VISITED_ALL) then
		return dist[pos][1]
	end

	if(dp[mask][pos] ~= -1) then
	   return dp[mask][pos]
	end


	-- Now from current node, we will try to go to every other node and take the min ans
	local ans = INT_MAX;

	-- Visit all the unvisited cities and take the best route
	for city=1, n do
		if(bitAND(mask,lshift(1,city))==0) then
			local newAns = dist[pos][city] + tsp(BitOR(mask,lshift(1,city)), city)
			if (newAns < ans) then
                cityOrder[pos] = city
                --print(cityOrder, newAns)
            end
            ans = math.min(ans, newAns)            
		end
	end
	dp[mask][pos] = ans 
	return ans
end

function path(mask, pos) --Encontra o caminho calculado
    if(mask==VISITED_ALL) then
        return
    end
    local ans = INT_MAX
    local chosenCity

    for city = 1, n do
        if(bitAND(mask, lshift(1, city))==0) then
            local newAns = dist[pos][city] + dp[BitOR(mask,lshift(1,city))][city]
            if(newAns < ans) then
                ans = newAns;
                chosenCity = city;
            end
        end

    end
    print(chosenCity) -- here you get the current city you need to visit
    path(BitOR(mask,lshift(1,chosenCity)),chosenCity)
end

function main()
    print ("Travelling Saleman Distance is ")
    print(tsp(1,1))
    print(path(1,1))
    simwait(1)

    return 0;
end
