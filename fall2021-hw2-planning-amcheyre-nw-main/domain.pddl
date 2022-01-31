(define (domain sokorobotto)
  (:requirements :typing)
  (:types location saleitem shipment order - objects
  robot pallette - device)
  (:predicates  
    (connected ?x ?y - location)
    (available ?x - location)
    (at ?x - device ?y - location)
    (packing-location ?x - location)
    (no-robot ?x - location)
    (no-pallette ?x - location)
    (free ?x - robot)
    (robot-pallette ?x - robot ?y - pallette)
    (contains ?x - pallette ?y - saleitem) 
    (unstarted ?x - shipment)
    (ships ?x - shipment ?y - order)
    (orders ?x - order ?y - saleitem)
    (includes ?x - shipment ?y - saleitem)
    (pallete-last-loc ?p - device ?x - location)
    (robot-last-loc ?r - device ?x - location)
  
  )

  (:action robot_looking_for_pallet
    :parameters (?o - order ?i - saleitem ?p - pallette ?loc1 ?loc2 ?loc3 - location ?r - robot ?s - shipment)
    :precondition (
      and (orders ?o ?i)
      (contains ?p ?i)
      (at ?p ?loc1)
      (at ?r ?loc2)
      (not(connected ?loc1 ?loc2))
      (connected ?loc2 ?loc3)
      (no-robot ?loc3)
      (not(no-pallette ?loc1))
      (unstarted ?s)
      (ships ?s ?o)
  

    )
    :effect (
      and (at ?r ?loc3)
      (not(robot-pallette ?r ?p))
      (not(no-robot ?loc3)) 
      (no-robot ?loc2)
    )
  )

  (:action robot_find_pallet
    :parameters (?o - order ?i - saleitem ?p - pallette ?loc1 ?loc2 - location ?r - robot ?s - shipment)
    :precondition (
      and (orders ?o ?i)
      (contains ?p ?i)
      (at ?p ?loc1)
      (at ?r ?loc2)
      (connected ?loc1 ?loc2)
      (unstarted ?s)
      (ships ?s ?o)
      (no-robot ?loc1)
  
    )
    :effect (
      and (at ?r ?loc1)
      (robot-pallette ?r ?p)
      (no-robot ?loc2)
      (not(no-robot ?loc1))
      (not(no-pallette ?loc1))
 

    )
  )
  
  
  (:action robot_taking_pallet_near_packing
    :parameters (?o - order ?i - saleitem ?p - pallette ?loc1 ?loc2 ?pack - location ?r - robot ?s - shipment) 
    :precondition (
      and (orders ?o ?i)
      (contains ?p ?i)
      (at ?p ?loc1)
      (at ?r ?loc1)
      (packing-location ?pack)
      (available ?pack)
      (not(connected ?loc1 ?pack))
      (connected ?loc1 ?loc2)
      (no-robot ?loc2)
      (no-pallette ?loc2)
      (ships ?s ?o)
      

    )
    :effect (
      and (at ?r ?loc2)
      (at ?p ?loc2)
      (not(no-robot ?loc2))
      (not(no-pallette ?loc2))
      (no-robot ?loc1)
      (no-pallette ?loc1)
      (robot-pallette ?r ?p)
      (pallete-last-loc ?p ?loc1)
      (robot-last-loc ?r ?loc1)

    )

  )

  (:action robot_move_pallet_into_packing
    :parameters (?o - order ?i - saleitem ?p - pallette ?loc1 ?pack - location ?r - robot ?s - shipment) 
    :precondition (
      and (orders ?o ?i)
      (contains ?p ?i)
      (at ?p ?loc1)
      (at ?r ?loc1)
      (packing-location ?pack)
      (available ?pack)
      (connected ?loc1 ?pack)
      (no-robot ?pack)
      (no-pallette ?pack)
      (unstarted ?s)
      (ships ?s ?o)
   

    )
    :effect (
      and (at ?r ?pack)
      (at ?p ?pack)
      (not(available ?pack))
      (no-robot ?loc1)
      (no-pallette ?loc1)
      (robot-pallette ?r ?p)
      (not(no-robot ?pack))
      (not(no-pallette ?pack))
      (pallete-last-loc ?p ?loc1)
      (robot-last-loc ?r ?loc1)
    )

  )

  (:action include_item
    :parameters (?o - order ?i - saleitem ?p - pallette ?pack - location ?r - robot ?s - shipment)
    :precondition (
      and (orders ?o ?i)
      (contains ?p ?i)
      (robot-pallette ?r ?p)
      (packing-location ?pack)
      (at ?r ?pack)
      (at ?p ?pack)
      (unstarted ?s)
      (ships ?s ?o)
      
    )
    :effect (
      and (includes ?s ?i)
      (not(available ?pack))
     

    )

  )
  
  (:action robot_remove_pallet_out_packing
    :parameters (?o - order ?i - saleitem ?p - pallette ?loc1 ?pack ?pack2 - location ?r - robot ?s - shipment)
    :precondition (
      and (not(available ?pack))
      (packing-location ?pack)
      (at ?r ?pack)
      (at ?p ?pack)
      (connected ?pack ?loc1)
      
      (no-pallette ?loc1)
     
      (includes ?s ?i)
      (orders ?o ?i)
      (contains ?p ?i)
      
      
     
      
    )
    :effect (
      and (at ?r ?loc1)
      (at ?p ?loc1)
      (no-robot ?pack)
      (no-pallette ?pack)
      (not(no-robot ?loc1))
      (not(no-pallette ?loc1))
      (available ?pack)
      (pallete-last-loc ?p ?pack)
      (robot-last-loc ?r ?pack)
     
    )
  )  

  (:action robot_remove_pallet_out_looking_for_store
    :parameters (?o - order ?i - saleitem ?p - pallette ?loc1 ?loc2 - location ?r - robot ?s - shipment)
    :precondition (
      and (robot-pallette ?r ?p)
      (at ?r ?loc1)
      (at ?p ?loc1)
      (connected ?loc1 ?loc2)
      (no-pallette ?loc2)
      (includes ?s ?i)
      (orders ?o ?i)
      (contains ?p ?i)
      (not(unstarted ?s))
      (not(packing-location ?loc2))
      (not(pallete-last-loc ?p ?loc2))
      (not(robot-last-loc ?r ?loc2))

    )
    :effect (
      and (at ?r ?loc2)
      (at ?p ?loc2)
      (no-robot ?loc1)
      (no-pallette ?loc1)
      (not(no-robot ?loc2))
      (not(no-pallette ?loc2))
      (pallete-last-loc ?p ?loc1)
      (robot-last-loc ?r ?loc1)
      
      
    )
  )
  
  (:action include_item2
    :parameters (?o - order ?i - saleitem ?p - pallette ?pack - location ?r - robot ?s - shipment)
    :precondition
      (and
        (packing-location ?pack)
        (at ?p ?pack)
        (available ?pack)
        (not(includes ?s ?i))
        (unstarted ?s)
      )
    :effect
      (and
        (includes ?s ?i)
        (not(contains ?p ?i))
        
      )
  )

)