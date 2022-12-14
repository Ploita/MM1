clear
#M/M/1

rng(1233) #semente
tempo_sim = 0.00 #tempo de simulação
estado_servidor = 1 #Disponível (1) ou ocupado (0)
pacotes_total = 50 #total de iterações a serem feitas
pacotes_simulados = 0 #total de iterações realizadas
media_chegada = 0.011   #tempo médio de chegada normal
media_service =0.01     #tempo médio de serviço
time_server_free = 0 #tempo do serviço ocupado
atraso_total = 0   #tempo total de atraso
tempo_fila = 0     #tempo total em fila
ite=1 #iterado para o memorial descritivo
descrito = zeros(50,2) #memorial descritivo

quadro = [(1:4)' zeros(4,1)]   #lista de eventos com prioridade
quadro(4,2) = Inf                                           # Próximo evento de saída
quadro(3,2) = exprnd(media_chegada)    # Próximo evento de entrada com prioridade alta
quadro(2,2) = exprnd(media_chegada)    # Próximo evento de entrada com prioridade média
quadro(1,2) = exprnd(media_chegada)    # Próximo evento de entrada com prioridade baixa

#Inicialização das filas de prioridade e dimensão das filas
fila_low = zeros(50,1)
q_low = 0
fila_med = zeros(50,1)
q_med = 0
fila_high = zeros(50,1)
q_high = 0
#
while(pacotes_simulados < pacotes_total)
    
    #Verificação do evento mais próximo
    [temp,pri] = min(quadro(:,2))
    #atualização do tempo dos próximos eventos
    quadro(:,2) = quadro(:,2) - temp
    
    #Cálculo da utilização
    if (estado_servidor)
        time_server_free = time_server_free + temp
    end
    
    #Cálculo do tempo de fila
    tempo_fila = tempo_fila + q_low*temp + q_med*temp + q_high*temp
    #Atualização do tempo de simulação
    tempo_sim = tempo_sim + temp
    #Atualização do memorial descritivo
    descrito(ite,:) = [tempo_sim,pri]
    ite=ite+1
    
    if(pri==4) #evento de saída
        #Pacote já saiu, busca de novo pacote por prioridade
        if q_high > 0
                
                atraso_total = atraso_total + tempo_sim - fila_high(1)
                for i = 1:q_high
                    fila_high(i)=fila_high(i+1)
                end
                q_high = q_high - 1
        quadro(4,2) = exprnd(media_service)
            
        elseif q_med > 0
                
                atraso_total = atraso_total + tempo_sim - fila_med(1)
                for i = 1:q_med
                    fila_med(i)=fila_med(i+1)
                end
                q_med = q_med - 1
        quadro(4,2) = exprnd(media_service)
            
        elseif q_low > 0
                
                atraso_total = atraso_total + tempo_sim - fila_low(1)
                for i = 1:q_low
                    fila_low(i)=fila_low(i+1)
                end
                q_low = q_low - 1
        quadro(4,2) = exprnd(media_service)
        
        else
            estado_servidor = 1
            quadro(4,2) = Inf
        end
        
    elseif (pri == 3) #Prioridade alta
        #Se o servidor estiver disponível não entra na fila
        if(estado_servidor)
            quadro(4,2) = exprnd(media_service)
            estado_servidor = 0
        else
            #Aumenta o tamanho da fila
            q_high = q_high + 1
            fila_high(q_high) = tempo_sim
        end
        quadro(3,2) = exprnd(media_chegada)

        pacotes_simulados = pacotes_simulados +1
        
    elseif (pri == 2) #Prioridade média
        if(estado_servidor)
            quadro(4,2) = exprnd(media_service)
            estado_servidor = 0
        else
            q_med = q_med + 1
            fila_med(q_med) = tempo_sim
        end
        quadro(2,2) = exprnd(media_chegada)
        
        pacotes_simulados = pacotes_simulados +1
        
    else #Prioridade baixa
        if(estado_servidor)
            quadro(4,2) = exprnd(media_service)
            estado_servidor = 0
        else
            q_low = q_low + 1
            fila_low(q_low) = tempo_sim
        end
        quadro(1,2) = exprnd(media_chegada)
        
        pacotes_simulados = pacotes_simulados +1
        
    end
    queue_size(ite,:) = [q_high q_med q_low]
end

fila_ttl = 1

quadro(3,2) = Inf
quadro(2,2) = Inf
quadro(1,2) = Inf

while(fila_ttl)
    fila_ttl = q_high + q_med + q_low
    #Verificação do evento mais próximo
    [temp,pri] = min(quadro(:,2))
    #atualização do tempo dos próximos eventos
    quadro(:,2) = quadro(:,2) - temp
    
    #Cálculo da utilização
    if (estado_servidor)
        time_server_free = time_server_free + temp
    end
    
    #Cálculo do tempo de fila
    tempo_fila = tempo_fila + q_low*temp + q_med*temp + q_high*temp
    #Atualização do tempo de simulação
    tempo_sim = tempo_sim + temp
    #Atualização do memorial descritivo
    descrito(ite,:) = [tempo_sim,pri]
    ite=ite+1
    
    if(pri==4) #evento de saída
        
        #Pacote já saiu, busca de novo pacote por prioridade
        if q_high > 0
                
                atraso_total = atraso_total + tempo_sim - fila_high(1)
                for i = 1:q_high
                    fila_high(i)=fila_high(i+1)
                end
                q_high = q_high - 1
        quadro(4,2) = exprnd(media_service)
            
        elseif q_med > 0
                
                atraso_total = atraso_total + tempo_sim - fila_med(1)
                for i = 1:q_med
                    fila_med(i)=fila_med(i+1)
                end
                q_med = q_med - 1
        quadro(4,2) = exprnd(media_service)
            
        elseif q_low > 0
                
                atraso_total = atraso_total + tempo_sim - fila_low(1)
                for i = 1:q_low
                    fila_low(i)=fila_low(i+1)
                end
                q_low = q_low - 1
        quadro(4,2) = exprnd(media_service)
        
        else
            estado_servidor = 1
            quadro(4,2) = Inf
        end

    end
    queue_size(ite,:) = [q_high q_med q_low]
     
end

plot(1:ite,queue_size)
xlim([1 ite])