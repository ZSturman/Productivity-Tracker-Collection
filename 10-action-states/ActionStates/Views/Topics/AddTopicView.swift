//
//  AddTopicView.swift
//  ActionStates
//
//  Created by Zachary Sturman on 7/25/23.
//

import CoreData
import SwiftUI

struct AddTopicView: View {
    @StateObject var topicViewModel: TopicViewModel
    
    @Environment(\.dismiss) var dismiss
    
    init(moc: NSManagedObjectContext) {
        _topicViewModel = StateObject(wrappedValue: TopicViewModel(moc: moc))
    }
    
    
    
    
    
    @State private var topicName = ""
    @State private var topicDescription = ""
    
    var body: some View {
        Form {
            Section {
                TextField("Topic Name", text: $topicViewModel.topicName)
            }
            Section {
                TextField("Topic Description", text: $topicViewModel.topicDescription)
            }
            
            Section {
                Button("Save") {
                    topicViewModel.addNewTopic()
                    dismiss()
                }
            }

        }
    }
}
