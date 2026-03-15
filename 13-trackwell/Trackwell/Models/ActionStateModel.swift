//
//  ActionStateModel.swift
//  Trackwell
//
//  Created by Zachary Sturman on 8/28/23.
//

import SwiftUI

class ActionState: Identifiable, ObservableObject {
    var id = UUID()
    var title: String
    var isAction: Bool
    var dateCreated: Date
    var dateUpdated: Date
    var triggers: [Trigger] = []
    var executions: [Execution] = []

    init(title: String, isAction: Bool, dateCreated: Date = Date(), dateUpdated: Date = Date()) {
        self.title = title
        self.isAction = isAction
        self.dateCreated = dateCreated
        self.dateUpdated = dateUpdated
    }
}
