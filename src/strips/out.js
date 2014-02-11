{'define': [
            {'domain': ['dock-worker-robot-pos']},
            {':requirements': null}, 
            {':types': ['location', 'pile', 'robot', 'crane', 'container']},
            {':constants': ['pallet', '-', 'container']},
            {':predicates': [
                             {'adjacent': ['?l1', '?l2', '-', 'location']},
                             {'attached': ['?p', '-', 'pile', '?l', '-', 'location']},
                             {'belong': ['?k', '-', 'crane', '?l', '-', 'location']},
                             {'at': ['?r', '-', 'robot', '?l', '-', 'location']},
                             {'free': ['?l', '-', 'location']},
                             {'loaded': ['?r', '-', 'robot', '?c', '-', 'container']},
                             {'unloaded': ['?r', '-', 'robot']},
                             {'holding': ['?k', '-', 'crane', '?c', '-', 'container']},
                             {'empty': ['?k', '-', 'crane']},
                             {'in': ['?c', '-', 'container', '?p', '-', 'pile']},
                             {'top': ['?c', '-', 'container', '?p', '-', 'pile']},
                             {'on': ['?k1', '-', 'container', '?k2', '-', 'container']}]
            },
	         {':parameters': [{'?r': ['-', 'robot', '?from', '?to', '-', 'location']}],
	          ':action': ['move'],
	          ':precondition': [{'and': [
	                                     {'adjacent': ['?from', '?to']},
	                                     {'at': ['?r', '?from']},
	                                     {'free': ['?to']}
	                                     ]
	                            }],
	          ':effect': [{'and': [
	                               {'at': ['?r', '?to']}, 
	                               {'free': ['?from']},
	                               {'not': [{'free': ['?to']}]}, 
	                               {'not': [{'at': ['?r', '?from']}]}]
	                      }]
	         },
	         {':parameters': [{'?k': ['-', 'crane', '?l', '-', 'location', '?c', '-', 'container', '?r', '-', 'robot']}], 
	          ':action': ['load'], 
	          ':precondition': [{'and': [
	        	                            {'at': ['?r', '?l']},
	        	                            {'belong': ['?k', '?l']}, 
	        	                            {'holding': ['?k', '?c']}, 
	        	                            {'unloaded': ['?r']}]
	        	                }], 
	          ':effect': [{'and': [
	                                    {'loaded': ['?r', '?c']},
	                                    {'not': [{'unloaded': ['?r']}]},
	                                    {'empty': ['?k']},
	                                    {'not': [{'holding': ['?k', '?c']}]}
	                              ]
	                      }]
	         },
	         {':parameters': [{'?k': ['-', 'crane', '?l', '-', 'location', '?c', '-', 'container', '?r', '-', 'robot']}],
	          ':action': ['unload'],
	          ':precondition': [{'and': [
	                                        {'belong': ['?k', '?l']},
	                                        {'at': ['?r', '?l']}, 
	                                        {'loaded': ['?r', '?c']},
	                                        {'empty': ['?k']}]
	                               }],
	          ':effect': [{'and': [
	                                {'unloaded': ['?r']},
	                                {'holding': ['?k', '?c']},
	                                {'not': [{'loaded': ['?r', '?c']}]}, 
	                                {'not': [{'empty': ['?k']}]}
	                                ]
	                       }]
	           },
	           {':parameters': [{'?k': ['-', 'crane', '?l', '-', 'location', '?c', '?else', '-', 'container', '?p', '-', 'pile']}], 
	        	':action': ['take'], 
	        	':precondition': [{'and': [{'belong': ['?k', '?l']}, {'attached': ['?p', '?l']}, {'empty': ['?k']}, {'in': ['?c', '?p']}, {'top': ['?c', '?p']}, {'on': ['?c', '?else']}]}], 
	        	':effect': [{'and': [{'holding': ['?k', '?c']}, {'top': ['?else', '?p']}, {'not': [{'in': ['?c', '?p']}]}, {'not': [{'top': ['?c', '?p']}]}, {'not': [{'on': ['?c', '?else']}]}, {'not': [{'empty': ['?k']}]}]}]}, 
	        {
	        	':parameters': [{'?k': ['-', 'crane', '?l', '-', 'location', '?c', '?else', '-', 'container', '?p', '-', 'pile']}], 
	        	':action': ['put'], 
	        	':precondition': [{'and': [{'belong': ['?k', '?l']}, {'attached': ['?p', '?l']}, {'holding': ['?k', '?c']}, {'top': ['?else', '?p']}]}], ':effect': [{'and': [{'in': ['?c', '?p']}, {'top': ['?c', '?p']}, {'on': ['?c', '?else']}, {'not': [{'top': ['?else', '?p']}]}, {'not': [{'holding': ['?k', '?c']}]}, {'empty': ['?k']}]}]
	        }
           ]
};