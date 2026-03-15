//
//  ActionStateDetailsTab.swift
//  BeingAnalytics
//
//  Created by Zachary Sturman on 9/15/23.
//

import SwiftUI

struct ActionStateDetailsTab: View { 
    
    var actionState: ActionState
    
    var dateCreated: String
    var dateUpdated: String
    
    init(actionState: ActionState) {
        self.actionState = actionState
        if let createdDate = actionState.dateCreated {
            self.dateCreated = FormattingHelper.shortenDateWithYear(createdDate)
        } else {
            self.dateCreated = "Unknown Date"
        }
        
        if let updatedDate = actionState.dateUpdated {
            self.dateUpdated = FormattingHelper.shortenDateWithYear(updatedDate)
        } else {
            self.dateUpdated = "Unknown Date"
        }
    }
    
    var body: some View {
        List {
            LabeledContent(content: {
                Text(actionState.title ?? "ActionState title unknown")
            }, label: {
                Text("Title:")
            })
            
            LabeledContent(content: {
                if actionState.isAction {
                    Text("Action")
                } else {
                    Text("State")
                }
                
            }, label: {
                Text("Category:")
            })
            
            LabeledContent(content: {
                Text(dateCreated)
            }, label: {
                Text("Created:")
            })
            
            LabeledContent(content: {
                Text(dateUpdated)
            }, label: {
                Text("Updated:")
            })
            
            LabeledContent(content: {
                Text("\(actionState.executions?.count ?? 0)")
            }, label: {
                Text("Executions:")
            })
            
            LabeledContent(content: {
                Text("\(actionState.globalVariables?.count ?? 0)")
            }, label: {
                Text("Global variables:")
            })
            
            LabeledContent(content: {
                Text("\(actionState.triggers?.count ?? 0)")
            }, label: {
                Text("Triggers:")
            })
            
            LabeledContent(content: {
                Text("\(actionState.inputs?.count ?? 0)")
            }, label: {
                Text("Inputs:")
            })
            
        }
    }
}
